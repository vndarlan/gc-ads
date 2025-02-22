import streamlit as st
import pandas as pd
import sys
import os
from db_utils import fetch_data, insert_data, overwrite_table_with_df

# Adiciona o diretório raiz (pai de "pages") ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def app():
    st.title("Gerenciar Páginas e Contas de Anúncio")

    with st.form("add_form"):
        st.subheader("Adicionar nova Página/Conta")
        nome_pagina = st.text_input("Nome da Página:")
        conta_anuncio = st.text_input("Nome/Apelido da Conta de Anúncio:")
        token_pagina = st.text_input("Token da Página (se precisar enviar no payload):")
        id_pagina = st.text_input("ID da Página Facebook:")
        id_conta_anuncio = st.text_input("ID da Conta de Anúncio Facebook:")

        if st.form_submit_button("Adicionar"):
            if not nome_pagina.strip() or not conta_anuncio.strip():
                st.error("Nome da Página e Conta de Anúncio são obrigatórios!")
            else:
                insert_data(nome_pagina, conta_anuncio, token_pagina, id_pagina, id_conta_anuncio)
                st.success("Página/Conta adicionada com sucesso!")

    st.write("---")
    st.subheader("Tabela de Dados Cadastrados")

    df = fetch_data()
    if df.empty:
        st.info("Não há dados cadastrados ainda.")
        return

    # Oculta coluna 'id' ao exibir no editor
    df_sem_id = df.drop(columns=["id"])

    # Editor com st.experimental_data_editor (Streamlit >= 1.22)
    df_editado = st.experimental_data_editor(
        df_sem_id,
        num_rows="dynamic",
        key="data_editor_gerenciar"
    )

    # Ao salvar, sobrescreve a tabela no BD
    if st.button("Salvar Alterações"):
        overwrite_table_with_df(df_editado)
        st.success("Dados atualizados com sucesso!")

def main():
    app()
