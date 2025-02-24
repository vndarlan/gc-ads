# Facebook.py (na pasta pages)
import streamlit as st
import requests
import sys
import os
import datetime
import pandas as pd

# Configura a página para largura completa
st.set_page_config(page_title="GC IA & Automações", layout="centered")

# Configurar caminhos para importação
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_utils import fetch_data, insert_data, overwrite_table_with_df

# URL do seu Webhook (ajuste se necessário)
WEBHOOK_URL = "https://primary-production-7d92.up.railway.app/webhook/f708e609-9e8b-4940-9cec-55c8cdceb2f7"

def inicializar_estado():
    """Inicializa todas as variáveis de sessão necessárias."""
    estados_necessarios = {
        'show_config': False,
        'dados_carregados': False,
        'debug_mode': False,
        'conta_info': None,
        'nome_video': "",           # Inicializado para evitar erro de atributo inexistente
        'nome_imagem_anuncio': ""   # Inicializado para evitar erro de atributo inexistente
    }
    for chave, valor in estados_necessarios.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor

def main():
    try:
        inicializar_estado()
        st.title("📢 Criar Nova Campanha")
        if st.session_state.debug_mode:
            st.write("Estado da sessão:", st.session_state)
        carregar_e_exibir_formulario()
    except Exception as e:
        st.error(f"Erro crítico: {str(e)}")
        st.stop()

def carregar_e_exibir_formulario():
    try:
        df = fetch_data()
        if df.empty:
            st.warning("Nenhuma página cadastrada. Primeiro cadastre em 'Gerenciar Páginas'.")
            return

        pagina_selecionada = st.selectbox("Selecione a Página:", df['nome_pagina'].unique(), key='seletor_pagina')
        st.session_state.pagina_selecionada = pagina_selecionada

        # Campo para definir a quantidade de conjuntos de anúncios (fora do formulário para ser reativo)
        if 'qtd_conjuntos' not in st.session_state:
            st.session_state.qtd_conjuntos = 1
        st.session_state.qtd_conjuntos = st.number_input(
            "Quantidade de Conjuntos de Anúncios", 
            min_value=1, max_value=10, 
            value=st.session_state.qtd_conjuntos, 
            step=1, 
            key='qtd_conjuntos_input'
        )

        if st.button("Iniciar Nova Campanha", key='btn_nova_campanha'):
            st.session_state.show_config = True

        if st.session_state.show_config:
            with st.form(key="form_campanha", clear_on_submit=True):
                st.subheader("Configurações da Campanha")
                
                # Obter informações da conta selecionada
                conta_info = obter_info_conta(df, pagina_selecionada)

                # Seções do formulário
                secao_config_basicas(conta_info)
                secao_publico_alvo()
                secao_conteudo_criativo()
                secao_config_avancadas()
                secao_conjuntos_anuncios()  # Utiliza st.session_state.qtd_conjuntos

                col1, col2, col3 = st.columns([1, 1, 2])
                with col2:
                    if st.form_submit_button("Salvar Rascunho"):
                        salvar_rascunho()
                with col3:
                    if st.form_submit_button("Publicar Campanha"):
                        publicar_campanha()
    except Exception as e:
        st.error(f"Falha ao carregar dados: {str(e)}")

def obter_info_conta(df, pagina_selecionada):
    """Obtém as informações da conta selecionada a partir do DataFrame."""
    df_filtrado = df[df['nome_pagina'] == pagina_selecionada]
    if df_filtrado.empty:
        raise ValueError("Nenhuma conta encontrada para a página selecionada.")
    
    conta_selecionada = st.selectbox("Selecione a Conta:", df_filtrado['conta_anuncio'].unique(), key='seletor_conta')
    return df_filtrado[df_filtrado['conta_anuncio'] == conta_selecionada].iloc[0]

def secao_config_basicas(conta_info):
    """Configurações Básicas da Campanha."""
    with st.expander("⚙️ Configurações Básicas", expanded=True):
        st.text_input("Nome da Campanha*", key='nome_campanha')
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Objetivo*", ["Vendas"], disabled=True, key='objetivo')
        with col2:
            st.radio("Tipo de Orçamento*", ["Diário"], horizontal=True, disabled=True, key='tipo_orcamento')
        st.number_input("Valor do Orçamento (em centavos)*", min_value=1000, value=2000, step=1000, key='valor_orcamento')
        
        # Novos campos
        st.text_input("Nome do Conjunto de Anúncios", key='nome_conjunto_anuncios')
        st.text_input("Pixel", key='pixel')
        st.selectbox("Evento de Conversão", options=["Compra"], disabled=True, key='evento_conversao')
        st.text_input("Campanha", value="Leilao", disabled=True, key='campanha')
        
        # Armazenar informações da conta no session_state
        st.session_state.account_id = conta_info['id_conta_anuncio']
        st.session_state.page_token = conta_info['token_pagina']
        st.session_state.conta_info = {
            'id_pagina': conta_info['id_pagina'],
            'vencimento_do_token': conta_info['vencimento_do_token'],
            'id_conta_anuncio': conta_info['id_conta_anuncio'],
            'conta_anuncio': conta_info['conta_anuncio']
        }

def secao_publico_alvo():
    """Configurações de Público-Alvo com aba de Idioma."""
    with st.expander("🎯 Público-Alvo", expanded=True):
        tab_dados, tab_idioma = st.tabs(["Dados", "Idioma"])
        with tab_dados:
            st.multiselect("Países*", ["MX", "ES", "CO", "CL", "EC", "GR"], default=["MX"], key='paises')
            col1, col2 = st.columns(2)
            with col1:
                st.slider("Faixa Etária*", 18, 65, (25, 45), key='faixa_etaria')
            with col2:
                st.radio("Gênero*", ["1, 2", "1", "2"], horizontal=True, key='genero')
        with tab_idioma:
            st.selectbox("Idioma", options=["6", "8", "16", "23", "53"], key='idioma')

def secao_conteudo_criativo():
    """Conteúdo Criativo da Campanha (sem upload de imagem, apenas nome)."""
    with st.expander("🎨 Conteúdo Criativo", expanded=True):
        # Campo para o nome do vídeo principal
        st.text_input("Nome do Anúncio", key='nome_video')
        
        # 5 caixas de texto grandes para os Textos Principais
        for i in range(1, 6):
            st.text_area(
                f"Texto Principal {i}",
                height=100,
                placeholder="Digite o texto do anúncio...",
                key=f"texto_principal_{i}"
            )

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("URL de Destino*", placeholder="https://seusite.com/oferta", key='url_destino')
        with col2:
            st.text_input("URL de Exibição", value="https://seusite.com", key='url_exibicao')
        
        # Campo para o nome da imagem do anúncio
        st.text_input("Nome da Imagem do Anúncio*", key='nome_imagem_anuncio')

def secao_config_avancadas():
    """Configurações Avançadas (valores fixos e não opcionais)."""
    with st.expander("🔧 Configurações Avançadas"):
        st.text_input("Posicionamento", value="Posicionamento Manual → Dispositivos: Celular", disabled=True, key='posicionamento')
        st.text_input("Conexão", value="Somente quando conectada a uma rede wifi", disabled=True, key='conexao_wifi')

def secao_conjuntos_anuncios():
    """Seção para definir os conjuntos de anúncios e seus respectivos vídeos."""
    with st.expander("📦 Conjuntos de Anúncios"):
        qtd = st.session_state.qtd_conjuntos
        for i in range(int(qtd)):
            st.text_input(f"Nome do Vídeo para Conjunto {i+1}", key=f"nome_video_conjunto_{i}")

def salvar_rascunho():
    """Simples feedback de salvamento de rascunho."""
    try:
        st.success("Rascunho salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar: {str(e)}")

def publicar_campanha():
    """Ao publicar, valida o formulário, constrói o payload e envia ao Webhook."""
    try:
        if validar_formulario():
            payload = construir_payload()
            enviar_webhook(payload)
            st.session_state.show_config = False
            st.success("Campanha publicada com sucesso!")
            st.balloons()
    except Exception as e:
        st.error(f"Erro na publicação: {str(e)}")

def validar_formulario():
    """Valida os campos obrigatórios do formulário."""
    erros = {}
    campos_obrigatorios = {
        'nome_campanha': 'Nome da campanha é obrigatório',
        'url_destino': 'URL de destino inválida',
        'nome_imagem_anuncio': 'Nome da imagem do anúncio é obrigatório',
        'objetivo': 'Selecione um objetivo',
        'tipo_orcamento': 'Selecione o tipo de orçamento'
    }
    for campo, mensagem in campos_obrigatorios.items():
        valor = st.session_state.get(campo)
        if not valor or (isinstance(valor, str) and not valor.strip()):
            erros[campo] = mensagem

    # Verifica se a URL de destino começa com http:// ou https://
    if st.session_state.url_destino and not st.session_state.url_destino.startswith(("http://", "https://")):
        erros['url_destino'] = "URL de destino deve começar com http:// ou https://"

    if erros:
        for erro in erros.values():
            st.error(erro)
        return False

    return True

def construir_payload():
    """Constrói o payload com todos os dados do formulário para envio ao webhook."""
    # Coleta os 5 textos principais
    textos_principais = []
    for i in range(1, 6):
        textos_principais.append(st.session_state.get(f"texto_principal_{i}", ""))

    # Dados dos conjuntos de anúncios
    qtd_conjuntos = int(st.session_state.get("qtd_conjuntos", 1))
    ad_sets = []
    for i in range(qtd_conjuntos):
        ad_set_video = st.session_state.get(f"nome_video_conjunto_{i}", "")
        ad_sets.append({"nome_video": ad_set_video})

    return {
        "metadata": {
            "timestamp": datetime.datetime.now().isoformat(),
            "versao": "2.1",
            "origin": "Streamlit App"
        },
        "configuracoes_conta": {
            "detalhes_pagina": {
                "nome_pagina": st.session_state.pagina_selecionada,
                "id_pagina": st.session_state.conta_info['id_pagina'],
                "token_pagina": st.session_state.page_token,
                "vencimento_token": st.session_state.conta_info['vencimento_do_token']
            },
            "detalhes_conta": {
                "nome_conta": st.session_state.conta_info['conta_anuncio'],
                "id_conta": st.session_state.account_id,
                "id_conta_anuncio": st.session_state.conta_info['id_conta_anuncio']
            }
        },
        "dados_campanha": {
            "basico": {
                "nome": st.session_state.nome_campanha,
                "objetivo": st.session_state.objetivo,
                "orcamento": {
                    "tipo": st.session_state.tipo_orcamento,
                    "valor": st.session_state.valor_orcamento,
                    "moeda": "BRL"
                },
                "nome_conjunto_anuncios": st.session_state.nome_conjunto_anuncios,
                "pixel": st.session_state.pixel,
                "evento_conversao": st.session_state.evento_conversao,
                "campanha": st.session_state.campanha
            },
            "publico_alvo": {
                "paises": st.session_state.paises,
                "idade": {
                    "min": st.session_state.faixa_etaria[0],
                    "max": st.session_state.faixa_etaria[1]
                },
                "genero": st.session_state.genero,
                "idioma": st.session_state.idioma
            },
            "criativo": {
                "nome_video": st.session_state.get("nome_video", ""),
                "textos_principais": textos_principais,
                "urls": {
                    "destino": st.session_state.url_destino,
                    "exibicao": st.session_state.url_exibicao
                },
                "midia": {
                    # Aqui enviamos apenas o nome do arquivo, sem upload/base64
                    "nome_arquivo": st.session_state.get("nome_imagem_anuncio", "")
                }
            },
            "configuracoes_avancadas": {
                "posicionamento": st.session_state.posicionamento,
                "conexao_wifi": st.session_state.conexao_wifi
            },
            "conjuntos_de_anuncios": ad_sets
        },
        "rastreamento": {
            "user_agent": st.query_params.get("user_agent", [""])[0],
            "ip_origem": st.query_params.get("ip", [""])[0]
        }
    }

def enviar_webhook(payload):
    """Envia os dados para o webhook e trata a resposta."""
    try:
        with st.spinner("Enviando dados..."):
            resposta = requests.post(WEBHOOK_URL, json=payload, timeout=15)
        if resposta.status_code == 200:
            st.success("Dados enviados com sucesso!")
            if st.session_state.debug_mode:
                st.json(payload)
        else:
            st.error(f"Erro na resposta: {resposta.status_code}")
            st.write("Detalhes do erro:", resposta.text)
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão: {str(e)}")
        if st.session_state.debug_mode:
            st.write("Payload que falhou:", payload)

if __name__ == "__main__":
    main()

