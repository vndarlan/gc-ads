import streamlit as st
import requests
import base64

# Configurações iniciais da página
st.set_page_config(page_title="GC ADS", page_icon="📢", layout="centered")

st.title("Criar Anúncio e Vincular à Página")

# --- Dicionário mapeando cada página para o respectivo webhook único ---
webhook_urls = {
    "🚧 Aqui en Chile (https://www.facebook.com/profile.php?id=61571024276758)": "https://primary-production-7d92.up.railway.app/webhook-test/f708e609-9e8b-4940-9cec-55c8cdceb2f7",
    "🚧 Aqui en Colômbia (https://www.facebook.com/profile.php?id=61570328387304)": "http://webhook.example.com/page2",
    "🚧 Chile Verificada (https://www.facebook.com/profile.php?id=61567114075779)": "http://webhook.example.com/page3",
    "🚧 Chile Verificada (https://www.facebook.com/profile.php?id=61561185936915)": "http://webhook.example.com/page4",
    "🚧 Chile Verificada (https://www.facebook.com/profile.php?id=61559099310185)": "http://webhook.example.com/page5",
    "Colômbia Verificada (https://www.facebook.com/profile.php?id=61551247163885)": "http://webhook.example.com/page6",
    "🚧 Equador Autenticada (https://www.facebook.com/profile.php?id=61561202461618)": "http://webhook.example.com/page7",
    "🚧 México Ahora (https://www.facebook.com/profile.php?id=61566808057808)": "http://webhook.example.com/page8",
    "🚧 México Comprovada (https://www.facebook.com/profile.php?id=61559137888697)": "http://webhook.example.com/page9",
    "🚧 Mexitudo (https://www.facebook.com/profile.php?id=61566655154283)": "http://webhook.example.com/page10",
    "🚧 Portugal Verificado (https://www.facebook.com/profile.php?id=61572970585528)": "http://webhook.example.com/page11",
    "🚧 Todo México (https://www.facebook.com/profile.php?id=61566371895032)": "http://webhook.example.com/page12",
}

# --- Seleção da Página ---
pages_options = list(webhook_urls.keys())
selected_page = st.selectbox("Selecione a página para vincular o anúncio:", pages_options)

# Gerencia estado para simular popup
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

# Botão para abrir o pseudo-popup (formulário)
if st.button("Novo Anúncio"):
    st.session_state.show_popup = True

st.markdown("<br>", unsafe_allow_html=True)  # Adiciona uma linha em branco


st.markdown("""
    <style>
        .titulo {
            background-color: #4CAF50;  /* Cor de fundo (verde neste exemplo) */
            color: white;  /* Cor do texto */
            padding: 10px;  /* Espaçamento interno */
            border-radius: 5px;  /* Bordas arredondadas */
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px; /* Espaço abaixo do título */
        }
    </style>
""", unsafe_allow_html=True)

# Só exibe o formulário se show_popup for True
if st.session_state.show_popup:
    # =========================================
    #  BLOCO 1: CRIANDO CAMPANHA
    # =========================================
    # Para exibir um título com fundo colorido:
    st.markdown('<div class="titulo">Criando Campanha</div>', unsafe_allow_html=True)

    # Campo para selecionar o nome da campanha (opções clicáveis)
    # Você pode personalizar a lista de opções de nomes de campanha
    opcoes_campanhas = ["Leilão - Conquista", "Leilão - Promoção", "Leilão - Marca"]
    campanha_selecionada = st.selectbox("Selecione o nome da campanha:", opcoes_campanhas)

    # Tipo de compra (fixo)
    st.write("**Tipo de compra:** Leilão")

    # Escolha um objetivo da campanha
    st.write("**Objetivo da campanha:** Vendas")

    # Configuração de campanha
    st.write("**Configuração de campanha:** Campanha de vendas manual")

    # Nome da Campanha (Sigla)
    nome_campanha_sigla = st.text_input("Nome da Campanha (Sigla):", "Ex: CC_CHILE_01")

    st.markdown("<br>", unsafe_allow_html=True)  # Adiciona uma linha em branco

    # =========================================
    #  BLOCO 2: CRIANDO CONJUNTO DE ANÚNCIOS
    # =========================================
    st.markdown('<div class="titulo">Criando Conjunto de Anúncios</div>', unsafe_allow_html=True)
    
    # Nome do Conjunto de Anúncios (Sigla)
    nome_conjunto = st.text_input("Nome do Conjunto de Anúncios (Sigla):", nome_campanha_sigla)

    # Local da conversão (fixo)
    st.write("**Local da conversão:** Site")

    # Conjunto de dados (Pixel)
    pixel = st.text_input("Conjunto de dados (Pixel):", "Ex: Pixel_Compra_1234")

    # Evento de Conversão (fixo)
    st.write("**Evento de Conversão**: Compra")

    # Orçamento Diário (R$)
    orcamento_diario = st.number_input("Orçamento Diário (R$):", min_value=0.0, value=20.0, step=1.0)

    # Localizações
    localizacoes = st.text_input("Localizações:", "Ex: País X, País Y")

    # Faixa de idade
    idade_min, idade_max = st.slider("Selecione a faixa de idade:", 18, 65, (22, 65))

    # Gênero
    genero = st.radio("Gênero:", ["Homens", "Mulheres", "Todos"])

    # Idiomas
    lista_idiomas = ["Português", "Espanhol", "Inglês", "Francês", "Alemão"]
    idioma_sel = st.selectbox("Idiomas:", lista_idiomas)

    # Posicionamentos (fixo)
    st.write("**Posicionamentos:** Posicionamentos manuais")

    # Dispositivos (fixo)
    st.write("**Dispositivos:** Celular")

    # Dispositivos móveis e SO específicos (fixo)
    st.write("**Somente quando conectado a uma rede Wi-Fi**")

    st.markdown("<br>", unsafe_allow_html=True)  # Adiciona uma linha em branco

    # =========================================
    #  BLOCO 3: CRIANDO ANÚNCIO
    # =========================================
    st.markdown('<div class="titulo">Criando Anúncio</div>', unsafe_allow_html=True)

    # Nome do anúncio
    nome_anuncio = st.text_input("Nome do anúncio:", "Ex: Anuncio_Promocional")

    # Nome do Criativo do Drive
    nome_criativo_drive = st.text_input("Nome do Criativo do Drive:", "Ex: drive_video_01")

    # URL do site
    url_site = st.text_input("URL do site:", "Ex: https://meusite.com/produtoX")

    # Link de exibição (link da homepage)
    link_exibicao = st.text_input("Link de exibição (homepage):", "Ex: https://meusite.com")

    # Resultados de pesquisa do facebook (Adicione o nome da imagem)
    nome_imagem_facebook = st.text_input("Resultados de pesquisa do Facebook (nome da imagem):", "Ex: imagem_promo.png")

    # Destino (referente a imagem)
    destino_imagem = st.text_input("Destino (referente à imagem):", "Ex: link para onde a imagem direciona")

    # Texto Principal (1 a 5) -> adicionar até 5 textos diferentes
    st.markdown("### Texto Principal (1 a 5)")
    texto_principal_list = []
    max_textos = 5
    for i in range(max_textos):
        txt = st.text_input(f"Texto principal #{i+1} (opcional):", key=f"texto_principal_{i}")
        if txt.strip():
            texto_principal_list.append(txt)

    st.markdown("<br>", unsafe_allow_html=True)  # Adiciona uma linha em branco

    # =========================================
    #  BLOCO 4: MÚLTIPLOS CONJUNTOS DE ANÚNCIO
    # =========================================
    st.markdown('<div class="titulo">Múltiplos Conjuntos de Anúncio</div>', unsafe_allow_html=True)

    adicionar_varios = st.checkbox("Adicionar mais de 1 conjunto de anúncio?")
    conjuntos = []
    if adicionar_varios:
        qtd = st.number_input("Quantos conjuntos adicionais?", min_value=1, max_value=10, value=1)
        for i in range(qtd):
            st.markdown(f"**Conjunto Extra {i+1}**")
            # Nome do Criativo
            nome_criativo_extra = st.text_input(f"Nome do Criativo {i+1}:", key=f"nome_criativo_{i+1}")
            conjuntos.append({
                "nome_criativo_drive": nome_criativo_extra
            })
            st.markdown("---")

    # BOTÃO FINAL - CRIAR ANÚNCIO
    if st.button("Criar Anúncio"):
        # Monta o payload
        payload = {
            "pagina": selected_page,
            "campanha": {
                "nome_campanha_selecionada": campanha_selecionada,  # Opções clicáveis
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

        # Obtém a URL do webhook com base na página selecionada
        webhook_url = webhook_urls.get(selected_page)

        st.write("**Payload enviado**:", payload)
        
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                st.success("Anúncio enviado com sucesso!")
            else:
                st.error(f"Erro ao enviar anúncio. Código: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Ocorreu um erro ao enviar o anúncio: {e}")
        
        # Fecha o pseudo-popup após enviar
        st.session_state.show_popup = False
