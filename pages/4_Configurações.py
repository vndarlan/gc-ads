# pages/1_Gerenciar_Paginas.py
import streamlit as st
import pandas as pd

from db_utils import fetch_data, insert_data, overwrite_table_with_df

def app():
    st.title("Gerenciar Páginas e Contas de Anúncio")

    # FORMULÁRIO para adicionar novas entradas
    with st.form("add_form"):
        st.subheader("Adicionar nova Página/Conta")
        nome_pagina = st.text_input("Nome da Página:")
        conta_anuncio = st.text_input("Nome/Apelido da Conta de Anúncio:")
        token_pagina = st.text_input("Token da Página (se precisar enviar no payload):")
        id_pagina = st.text_input("ID da Página Facebook:")
        id_conta_anuncio = st.text_input("ID da Conta de Anúncio Facebook:")

        if st.form_submit_button("Adicionar"):
            if nome_pagina.strip() == "" or conta_anuncio.strip() == "":
                st.error("Nome da Página e Conta de Anúncio são obrigatórios!")
            else:
                insert_data(
                    nome_pagina, conta_anuncio, token_pagina,
                    id_pagina, id_conta_anuncio
                )
                st.success("Página/Conta adicionada com sucesso!")

    st.write("---")
    st.subheader("Tabela de Dados Cadastrados")

    # Carrega do banco
    df = fetch_data()
    if df.empty:
        st.info("Não há dados cadastrados ainda.")
        return

    # Ocultamos a coluna 'id' para não bagunçar a edição
    df_display = df.drop(columns=["id"])

    # Editor que permite edição direta dos campos
    df_editado = st.experimental_data_editor(
        df_display,
        num_rows="dynamic",
        key="data_editor_gerenciar"
    )

    # Botão para salvar as edições no Postgres
    if st.button("Salvar Alterações"):
        overwrite_table_with_df(df_editado)
        st.success("Dados atualizados com sucesso!")

def main():
    app()
