import streamlit as st
import psycopg2
import pandas as pd

def get_connection():
    try:
        conn = psycopg2.connect(st.secrets["DATABASE_URL"])
        return conn
    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")
        raise

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

# --- Função fetch_data VERIFICADA ---
def fetch_data():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM paginas;")
            rows = cur.fetchall()
        return pd.DataFrame(
            rows,
            columns=["id","nome_pagina","conta_anuncio","token_pagina","id_pagina","id_conta_anuncio"]
        )
    finally:
        conn.close()

# ... (mantenha as outras funções como insert_data, etc)