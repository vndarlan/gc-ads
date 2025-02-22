# db_utils.py
import psycopg2
import pandas as pd
import streamlit as st

def get_connection():
    """
    Cria a conexão com o Postgres usando as credenciais
    guardadas em st.secrets.
    Certifique-se de ter configurado no Streamlit Cloud (Secrets)
    algo como:
    [DB]
    HOST = "..."
    PORT = "..."
    NAME = "..."
    USER = "..."
    PASSWORD = "..."
    """
    conn = psycopg2.connect(
        host=st.secrets["DB"]["HOST"],
        port=st.secrets["DB"]["PORT"],
        database=st.secrets["DB"]["NAME"],
        user=st.secrets["DB"]["USER"],
        password=st.secrets["DB"]["PASSWORD"],
    )
    return conn

def create_table_if_not_exists():
    """Cria a tabela 'paginas' se ainda não existir."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS paginas (
                id SERIAL PRIMARY KEY,
                nome_pagina TEXT,
                conta_anuncio TEXT,
                token_pagina TEXT,
                id_pagina TEXT,
                id_conta_anuncio TEXT
            );
            """
        )
        conn.commit()
    conn.close()

def fetch_data():
    """Retorna todas as linhas da tabela 'paginas' como um DataFrame pandas."""
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
    """Insere uma nova linha na tabela 'paginas'."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO paginas (nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio)
        )
        conn.commit()
    conn.close()

def overwrite_table_with_df(df_editado):
    """
    Limpa a tabela 'paginas' e insere tudo que estiver em df_editado.
    (Abordagem simples para sincronizar com o data_editor.)
    """
    conn = get_connection()
    with conn.cursor() as cur:
        # 1) Limpa tabela
        cur.execute("TRUNCATE TABLE paginas RESTART IDENTITY;")

        # 2) Reinsere tudo
        for i, row in df_editado.iterrows():
            cur.execute(
                """
                INSERT INTO paginas (nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio)
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
