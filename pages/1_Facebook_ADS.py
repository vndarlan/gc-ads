import streamlit as st
import requests
import sys
import os

# Adiciona o diretório pai ao Python Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import fetch_data, insert_data, overwrite_table_with_df  # Import absoluto

def app():
    st.title("Criar Anúncio")

    df = fetch_data()
    if df.empty:
        st.warning("Não há Páginas/Contas cadastradas. Vá em 'Gerenciar Páginas'.")
        return

    paginas_disponiveis = df["nome_pagina"].unique().tolist()
    selected_page = st.selectbox("Selecione a Página para vincular o anúncio:", paginas_disponiveis)

    df_page = df[df["nome_pagina"] == selected_page]
    contas_disponiveis = df_page["conta_anuncio"].unique().tolist()

    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    if st.button("Novo Anúncio"):
        st.session_state.show_popup = True

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <style>
        .titulo {
            background-color: #4CAF50;  
            color: white;  
            padding: 10px;  
            border-radius: 5px;  
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.show_popup:
        if len(contas_disponiveis) == 0:
            st.error("Não há contas de anúncio para esta página.")
            return

        st.markdown('<div class="titulo">Selecione a Conta Vinculada</div>', unsafe_allow_html=True)
        selected_account_name = st.selectbox("Conta de Anúncio:", contas_disponiveis)

        row = df_page[df_page["conta_anuncio"] == selected_account_name].iloc[0]
        selected_account_id = row["id_conta_anuncio"]
        selected_token = row["token_pagina"]

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 1: CRIANDO CAMPANHA
        st.markdown('<div class="titulo">Criando Campanha</div>', unsafe_allow_html=True)
        nome_campanha_sigla = st.text_input("Nome da Campanha (Sigla):", "Ex: CC_CHILE_01")

        # BLOCO 2: CRIANDO CONJUNTO DE ANÚNCIOS
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="titulo">Criando Conjunto de Anúncios</div>', unsafe_allow_html=True)

        nome_conjunto = st.text_input("Nome do Conjunto de Anúncios (Sigla):", nome_campanha_sigla)
        pixel = st.text_input("Conjunto de dados (Pixel):", "Ex: Pixel_Compra_1234")
        orcamento_diario = st.number_input("Orçamento Diário (R$):", min_value=0.0, value=20.0, step=1.0)
        localizacoes = st.text_input("Localizações:", "Ex: País X, País Y")

        idade_min, idade_max = st.slider("Faixa de idade:", 18, 65, (22, 65))
        genero = st.radio("Gênero:", ["Homens", "Mulheres", "Todos"])

        lista_idiomas = ["Português", "Espanhol", "Inglês", "Francês", "Alemão"]
        idioma_sel = st.selectbox("Idiomas:", lista_idiomas)

        # BLOCO 3: CRIANDO ANÚNCIO
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="titulo">Criando Anúncio</div>', unsafe_allow_html=True)

        nome_anuncio = st.text_input("Nome do anúncio:", "Ex: Anuncio_Promocional")
        url_site = st.text_input("URL do site:", "Ex: https://meusite.com/produtoX")
        nome_imagem_facebook = st.text_input("Nome da imagem do Facebook:", "Ex: imagem_promo.png")

        # BLOCO 4: Webhook
        universal_webhook_url = "https://primary-production-7d92.up.railway.app/webhook-test/f708e609-9e8b-4940-9cec-55c8cdceb2f7"

        if st.button("Criar Anúncio"):
            payload = {
                "pagina": selected_page,
                "conta_id": selected_account_id,
                "token_pagina": selected_token,
                "campanha": {
                    "nome_campanha_sigla": nome_campanha_sigla
                },
                "conjunto": {
                    "nome_conjunto_sigla": nome_conjunto,
                    "pixel": pixel,
                    "orcamento_diario": orcamento_diario,
                    "localizacoes": localizacoes,
                    "idade_min": idade_min,
                    "idade_max": idade_max,
                    "genero": genero,
                    "idioma": idioma_sel
                },
                "anuncio": {
                    "nome_anuncio": nome_anuncio,
                    "url_site": url_site,
                    "nome_imagem_facebook": nome_imagem_facebook
                }
            }

            try:
                response = requests.post(universal_webhook_url, json=payload)
                if response.status_code == 200:
                    st.success("Anúncio enviado com sucesso!")
                else:
                    st.error(f"Erro ao enviar anúncio. Código: {response.status_code}")
            except Exception as e:
                st.error(f"Ocorreu um erro ao enviar o anúncio: {e}")

            st.session_state.show_popup = False

if __name__ == "__main__":
    app()