import streamlit as st
import psycopg2
import pandas as pd

# ========== CONEXÃO ==========
def get_connection():
    try:
        return psycopg2.connect(st.secrets["DATABASE_URL"])
    except Exception as e:
        st.error(f"🚨 Erro de conexão: {str(e)}")
        raise

# ========== CRIAÇÃO DA TABELA ==========
def create_table_if_not_exists():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS paginas (
                    id SERIAL PRIMARY KEY,
                    nome_pagina TEXT NOT NULL,
                    conta_anuncio TEXT NOT NULL,
                    token_pagina TEXT,
                    vencimento_do_token TEXT,
                    id_pagina TEXT,
                    id_conta_anuncio TEXT
                );
            """)
            # Verifica e adiciona coluna se não existir
            cur.execute("""
                ALTER TABLE paginas 
                ADD COLUMN IF NOT EXISTS vencimento_do_token TEXT;
            """)
            conn.commit()
    except Exception as e:
        st.error(f"🚨 Erro ao criar tabela: {str(e)}")
    finally:
        if conn:
            conn.close()

# ========== FUNÇÕES CRUD ==========
def fetch_data():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM paginas;")
            # OBSERVAÇÃO:
            # Apesar da definição original dos campos (nome_pagina, conta_anuncio, token_pagina, vencimento_do_token, id_pagina, id_conta_anuncio),
            # o ALTER TABLE fez com que a coluna 'vencimento_do_token' ficasse no final da tabela.
            # Assim, a ordem real dos campos é:
            # [id, nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio, vencimento_do_token]
            return pd.DataFrame(
                cur.fetchall(),
                columns=["id", "nome_pagina", "conta_anuncio", "token_pagina", "id_pagina", "id_conta_anuncio", "vencimento_do_token"]
            )
    except Exception as e:
        st.error(f"🚨 Erro ao buscar dados: {str(e)}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def insert_data(nome_pagina, conta_anuncio, token_pagina, vencimento_do_token, id_pagina, id_conta_anuncio):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO paginas (
                    nome_pagina,
                    conta_anuncio,
                    token_pagina,
                    vencimento_do_token,
                    id_pagina,
                    id_conta_anuncio
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (nome_pagina, conta_anuncio, token_pagina, vencimento_do_token, id_pagina, id_conta_anuncio)
            )
            conn.commit()
        return True
    except Exception as e:
        st.error(f"🚨 Erro ao inserir dados: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def overwrite_table_with_df(df_editado):
    try:
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
                        vencimento_do_token,
                        id_pagina,
                        id_conta_anuncio
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        row["nome_pagina"],
                        row["conta_anuncio"],
                        row["token_pagina"],
                        row["vencimento_do_token"],
                        row["id_pagina"],
                        row["id_conta_anuncio"]
                    )
                )
            conn.commit()
        return True
    except Exception as e:
        st.error(f"🚨 Erro ao sobrescrever tabela: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()
