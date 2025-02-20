import streamlit as st
import requests

# Configuração da página
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
# Usa as chaves do dicionário para formar as opções do selectbox
pages_options = list(webhook_urls.keys())
selected_page = st.selectbox("Selecione a página para vincular o anúncio:", pages_options)

# --- Formulário para Coletar Dados do Anúncio ---
with st.form("form_anuncio"):
    st.subheader("Configurações do Anúncio")
    
    idioma = st.selectbox("Selecione o idioma do anúncio:", ["Português", "Inglês", "Espanhol"])
    pais = st.selectbox("Selecione o país:", ["Brasil", "Estados Unidos", "Colômbia"])
    descricao = st.text_area("Descrição do anúncio:")
    video_nome = st.text_input("Nome do vídeo:")
    
    submit = st.form_submit_button("Criar Anúncio")

# --- Envio dos Dados para o Webhook Específico ---
if submit:
    payload = {
        "pagina": selected_page,
        "idioma": idioma,
        "pais": pais,
        "descricao": descricao,
        "video_nome": video_nome,
    }
    
    # Obtém a URL do webhook com base na página selecionada
    webhook_url = webhook_urls.get(selected_page)
    
    st.write("Payload enviado:", payload)
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            st.success("Anúncio enviado com sucesso!")
        else:
            st.error(f"Erro ao enviar anúncio. Código: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Ocorreu um erro ao enviar o anúncio: {e}")
