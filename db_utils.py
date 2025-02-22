import streamlit as st
import psycopg2
import pandas as pd

def get_connection():
    db_url = st.secrets["DATABASE_URL"]  # Lê a string do secrets
    conn = psycopg2.connect(db_url)
    return conn

def create_table_if_not_exists():
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
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE paginas RESTART IDENTITY;")
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
