import streamlit as st
from db_utils import create_table_if_not_exists
import sys
import os

# Configuração do path para o VS Code
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    st.set_page_config(
        page_title="GC ADS",
        page_icon="📢",
        layout="centered",
        initial_sidebar_state="auto"
    )
    st.title("Página Inicial")
    st.write("Bem-vindo. Use o menu lateral para navegar.")
    create_table_if_not_exists()

if __name__ == "__main__":
    main()