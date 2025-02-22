# pages/2_Criar_Anuncio.py
import streamlit as st
import requests
from db_utils import fetch_data

def app():
    st.title("Criar Anúncio")

    # Carrega dados do banco
    df = fetch_data()
    if df.empty:
        st.warning("Não há Páginas/Contas cadastradas. Vá em 'Gerenciar Páginas'.")
        return

    # Selecionar a Página
    paginas_disponiveis = df["nome_pagina"].unique().tolist()
    selected_page = st.selectbox("Selecione a Página para vincular o anúncio:", paginas_disponiveis)

    # Filtra as contas daquela página
    df_page = df[df["nome_pagina"] == selected_page]
    contas_disponiveis = df_page["conta_anuncio"].unique().tolist()

    # Gerencia estado para pseudo-popup
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    if st.button("Novo Anúncio"):
        st.session_state.show_popup = True

    st.markdown("<br>", unsafe_allow_html=True)  # Linha em branco

    # CSS para títulos (exemplo)
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

    # Só exibe o formulário se show_popup == True
    if st.session_state.show_popup:
        # Caso não haja contas
        if len(contas_disponiveis) == 0:
            st.error("Não há contas de anúncio cadastradas para esta página.")
            return

        # =========================================
        # Selecionar Conta Vinculada
        # =========================================
        st.markdown('<div class="titulo">Selecione a Conta Vinculada</div>', unsafe_allow_html=True)
        selected_account_name = st.selectbox("Conta de Anúncio:", contas_disponiveis)

        # Pega os dados da conta selecionada
        row_selecionada = df_page[df_page["conta_anuncio"] == selected_account_name].iloc[0]
        selected_account_id = row_selecionada["id_conta_anuncio"]
        selected_token = row_selecionada["token_pagina"]
        # Se precisar do ID da página: row_selecionada["id_pagina"]

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================
        #  BLOCO 1: CRIANDO CAMPANHA
        # =========================================
        st.markdown('<div class="titulo">Criando Campanha</div>', unsafe_allow_html=True)
        st.write("**Tipo de compra:** Leilão")
        st.write("**Objetivo da campanha:** Vendas")
        st.write("**Configuração de campanha:** Campanha de vendas manual")

        nome_campanha_sigla = st.text_input("Nome da Campanha (Sigla):", "Ex: CC_CHILE_01")

        # =========================================
        #  BLOCO 2: CRIANDO CONJUNTO DE ANÚNCIOS
        # =========================================
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="titulo">Criando Conjunto de Anúncios</div>', unsafe_allow_html=True)

        nome_conjunto = st.text_input("Nome do Conjunto de Anúncios (Sigla):", nome_campanha_sigla)
        st.write("**Local da conversão:** Site")

        pixel = st.text_input("Conjunto de dados (Pixel):", "Ex: Pixel_Compra_1234")
        st.write("**Evento de Conversão**: Compra")

        orcamento_diario = st.number_input("Orçamento Diário (R$):", min_value=0.0, value=20.0, step=1.0)
        localizacoes = st.text_input("Localizações:", "Ex: País X, País Y")

        idade_min, idade_max = st.slider("Faixa de idade:", 18, 65, (22, 65))
        genero = st.radio("Gênero:", ["Homens", "Mulheres", "Todos"])

        lista_idiomas = ["Português", "Espanhol", "Inglês", "Francês", "Alemão"]
        idioma_sel = st.selectbox("Idiomas:", lista_idiomas)

        st.write("**Posicionamentos:** Manuais")
        st.write("**Dispositivos:** Celular")
        st.write("**Somente quando conectado a uma rede Wi-Fi**")

        # =========================================
        #  BLOCO 3: CRIANDO ANÚNCIO
        # =========================================
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="titulo">Criando Anúncio</div>', unsafe_allow_html=True)

        nome_anuncio = st.text_input("Nome do anúncio:", "Ex: Anuncio_Promocional")
        nome_criativo_drive = st.text_input("Nome do Criativo do Drive:", "Ex: drive_video_01")
        url_site = st.text_input("URL do site:", "Ex: https://meusite.com/produtoX")
        link_exibicao = st.text_input("Link de exibição (homepage):", "Ex: https://meusite.com")
        nome_imagem_facebook = st.text_input("Nome da imagem do Facebook:", "Ex: imagem_promo.png")
        destino_imagem = st.text_input("Destino (link da imagem):", "Ex: https://seusite.com")

        st.markdown("### Texto Principal (1 a 5)")
        texto_principal_list = []
        max_textos = 5
        for i in range(max_textos):
            txt = st.text_input(f"Texto principal #{i+1} (opcional):", key=f"texto_principal_{i}")
            if txt.strip():
                texto_principal_list.append(txt)

        # =========================================
        #  BLOCO 4: MÚLTIPLOS CONJUNTOS DE ANÚNCIO
        # =========================================
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="titulo">Múltiplos Conjuntos de Anúncio</div>', unsafe_allow_html=True)

        adicionar_varios = st.checkbox("Adicionar mais de 1 conjunto de anúncio?")
        conjuntos = []
        if adicionar_varios:
            qtd = st.number_input("Quantos conjuntos adicionais?", min_value=1, max_value=10, value=1)
            for i in range(qtd):
                st.markdown(f"**Conjunto Extra {i+1}**")
                nome_criativo_extra = st.text_input(f"Nome do Criativo {i+1}:", key=f"nome_criativo_{i+1}")
                conjuntos.append({"nome_criativo_drive": nome_criativo_extra})
                st.markdown("---")

        # URL do seu webhook
        universal_webhook_url = "https://minha-url-unica.com/webhook"

        # Botão Final
        if st.button("Criar Anúncio"):
            payload = {
                "pagina": selected_page,
                "conta_id": selected_account_id if selected_account_id else "",
                "token_pagina": selected_token if selected_token else "",
                "campanha": {
                    "tipo_compra": "Leilão",
                    "objetivo": "Vendas",
                    "configuracao_campanha": "Campanha de vendas manual",
                    "nome_campanha_sigla": nome_campanha_sigla
                },
                "conjunto": {
                    "nome_conjunto_sigla": nome_conjunto,
                    "local_conversao": "Site",
                    "pixel": pixel,
                    "evento_conversao": "Compra",
                    "orcamento_diario": orcamento_diario,
                    "localizacoes": localizacoes,
                    "idade_min": idade_min,
                    "idade_max": idade_max,
                    "genero": genero,
                    "idioma": idioma_sel,
                    "posicionamentos": "Manuais",
                    "dispositivos": "Celular",
                    "wifi_only": True
                },
                "anuncio": {
                    "nome_anuncio": nome_anuncio,
                    "nome_criativo_drive": nome_criativo_drive,
                    "url_site": url_site,
                    "link_exibicao": link_exibicao,
                    "nome_imagem_facebook": nome_imagem_facebook,
                    "destino_imagem": destino_imagem,
                    "textos_principais": texto_principal_list
                },
                "conjuntos_extra": conjuntos
            }

            st.write("**Payload enviado**:", payload)

            try:
                response = requests.post(universal_webhook_url, json=payload)
                if response.status_code == 200:
                    st.success("Anúncio enviado com sucesso!")
                else:
                    st.error(f"Erro ao enviar anúncio. Código: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Ocorreu um erro ao enviar o anúncio: {e}")

            # Fecha o pseudo-popup
            st.session_state.show_popup = False

def main():
    app()
