import streamlit as st
import psycopg2
import pandas as pd

def get_connection():
    """
    Conecta no Postgres usando uma única variável:
    st.secrets["DATABASE_URL"] (string de conexão completa).
    """
    db_url = st.secrets["DATABASE_URL"]  # Ex: "postgresql://user:pass@host:port/dbname"
    conn = psycopg2.connect(db_url)
    return conn

def create_table_if_not_exists():
    """
    Cria a tabela 'paginas' se ainda não existir.
    Ajuste colunas se necessário.
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
    Puxa todos os registros de 'paginas' e retorna em DataFrame.
    Colunas: id, nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio.
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
    Insere nova linha na tabela 'paginas'.
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO paginas (
                nome_pagina,
                conta_anuncio,
                token_pagina,
                id_pagina,
                id_conta_anuncio
            ) VALUES (%s, %s, %s, %s, %s)
            """,
            (nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio)
        )
        conn.commit()
    conn.close()

def overwrite_table_with_df(df_editado):
    """
    Exemplo simples: apaga tudo e reinsere conforme 'df_editado'.
    (Útil se estiver usando st.experimental_data_editor)
    """
    conn = get_connection()
    with conn.cursor() as cur:
        # Limpa tabela
        cur.execute("TRUNCATE TABLE paginas RESTART IDENTITY;")

        # Reinsere cada linha
        for _, row in df_editado.iterrows():
            cur.execute(
                """
                INSERT INTO paginas (
                    nome_pagina,
                    conta_anuncio,
                    token_pagina,
                    id_pagina,
                    id_conta_anuncio
                ) VALUES (%s, %s, %s, %s, %s)
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
