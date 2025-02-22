import streamlit as st
from db_utils import create_table_if_not_exists

def main():
    st.set_page_config(page_title="GC ADS", page_icon="📢", layout="centered")
    st.title("Bem-vindo ao Meu App de Anúncios")
    st.write("Navegue usando o menu lateral para gerenciar páginas ou criar anúncios.")

    # Garante que a tabela existe antes de usar
    create_table_if_not_exists()

if __name__ == "__main__":
    main()


