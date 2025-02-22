import streamlit as st
import psycopg2
import pandas as pd

def get_connection():
    """
    Abre conexão com o Postgres a partir de DATABASE_URL,
    que deve estar em st.secrets["DATABASE_URL"] no Streamlit Cloud.
    Exemplo no secrets.toml:
    
    DATABASE_URL = "postgresql://usuario:senha@host:porta/nome_do_banco"
    """
    db_url = st.secrets["DATABASE_URL"]
    conn = psycopg2.connect(db_url)
    return conn

def create_table_if_not_exists():
    """
    Exemplo de criação de tabela (você pode ajustar campos e tipos conforme seu caso).
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS paginas (
                id SERIAL PRIMARY KEY,
                nome_pagina TEXT,
                conta_anuncio TEXT,
                token_pagina TEXT,
                id_pagina TEXT,
                id_conta_anuncio TEXT
            );
        """)
        conn.commit()
    conn.close()

def fetch_data():
    """
    Retorna todas as linhas da tabela 'paginas' em um DataFrame pandas.
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM paginas;")
        rows = cur.fetchall()
    conn.close()

    df = pd.DataFrame(
        rows,
        columns=["id","nome_pagina","conta_anuncio","token_pagina","id_pagina","id_conta_anuncio"]
    )
    return df

def insert_data(nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio):
    """
    Insere uma nova linha na tabela 'paginas'.
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO paginas (
                nome_pagina, conta_anuncio,
                token_pagina, id_pagina, id_conta_anuncio
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio)
        )
        conn.commit()
    conn.close()

def overwrite_table_with_df(df_editado):
    """
    Limpa a tabela 'paginas' e reinsere tudo do df_editado.
    Abordagem simples para sincronizar com data_editor.
    """
    conn = get_connection()
    with conn.cursor() as cur:
        # 1) Limpa tabela
        cur.execute("TRUNCATE TABLE paginas RESTART IDENTITY;")

        # 2) Reinsere cada linha do DataFrame
        for _, row in df_editado.iterrows():
            cur.execute(
                """
                INSERT INTO paginas (
                    nome_pagina, conta_anuncio,
                    token_pagina, id_pagina, id_conta_anuncio
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    row["nome_pagina"],
                    row["conta_anuncio"],
                    row["token_pagina"],
                    row["id_pagina"],
                    row["id_conta_anuncio"]
                )
            )
        conn.commit()
    conn.close()
