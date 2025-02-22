import streamlit as st
from db_utils import create_table_if_not_exists

def main():
    st.write("secrets:", st.secrets)
    ...

def main():
    st.set_page_config(page_title="GC ADS", page_icon="📢", layout="centered")
    st.title("Página Inicial")
    st.write("Bem-vindo. Use o menu lateral para navegar.")
    create_table_if_not_exists()

if __name__ == "__main__":
    main()
