import streamlit as st
import requests

st.title("Criar Anúncio e Vincular à Página")

# --- Seleção da Página ---
# Cria uma lista com 15 páginas (você pode personalizar os nomes conforme necessário)
pages_options = [f"Página {i}" for i in range(1, 16)]
selected_page = st.selectbox("Selecione a página para vincular o anúncio:", pages_options)

# Dicionário mapeando cada página para o respectivo webhook único
webhook_urls = {
    "🚧 Aqui en Chile (url da página)": "https://primary-production-7d92.up.railway.app/webhook-test/f708e609-9e8b-4940-9cec-55c8cdceb2f7",
    "🚧 Aqui en Colômbia": "http://webhook.example.com/page2",
    "🚧 Chile Verificada": "http://webhook.example.com/page3",
    "🚧 Chile Verificada": "http://webhook.example.com/page4",
    "🚧 Chile Verificada": "http://webhook.example.com/page5",
    "Colômbia Verificada": "http://webhook.example.com/page6",
    "🚧 Equador Autenticada": "http://webhook.example.com/page7",
    "🚧 México Ahora": "http://webhook.example.com/page8",
    "🚧 México Comprovada": "http://webhook.example.com/page9",
    "🚧 Mexitudo": "http://webhook.example.com/page10",
    "🚧 Portugal Verificado": "http://webhook.example.com/page11",
    "🚧 Todo México": "http://webhook.example.com/page12",
}

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
