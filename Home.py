import streamlit as st
import requests

# Título da aplicação
st.title("Gerenciador de Anúncios - Integração n8n e Facebook")

# Criação do formulário
with st.form("form_anuncio"):
    st.subheader("Configurações do Anúncio")
    
    # Seleção do idioma
    idioma = st.selectbox("Selecione o idioma do anúncio:", ["Português", "Inglês", "Espanhol"])
    
    # Seleção do país
    pais = st.selectbox("Selecione o país:", ["Brasil", "Estados Unidos", "México"])
    
    # Campo de descrição do anúncio
    descricao = st.text_area("Descrição do anúncio:")
    
    # Upload do vídeo
    video = st.file_uploader("Envie o vídeo do anúncio", type=["mp4", "mov"])
    
    # Botão de submissão
    submit = st.form_submit_button("Criar Anúncio")

# Quando o formulário for submetido
if submit:
    # Monta os dados do payload para enviar ao n8n
    payload = {
        "idioma": idioma,
        "pais": pais,
        "descricao": descricao,
        # Aqui, dependendo da implementação do n8n, pode ser necessário tratar o upload do vídeo
        # Por exemplo, salvando temporariamente ou enviando como multipart/form-data.
    }
    
    st.write("Dados a serem enviados:", payload)
    
    # Exemplo de endpoint do n8n (substitua pela URL correta do seu webhook)
    url_n8n = "http://SEU_ENDPOINT_N8N/webhook"
    
    try:
        # Envia os dados para o n8n
        resposta = requests.post(url_n8n, json=payload)
        
        # Verifica a resposta
        if resposta.status_code == 200:
            st.success("Anúncio enviado com sucesso! O fluxo no n8n foi ativado.")
        else:
            st.error(f"Erro ao enviar anúncio. Código de status: {resposta.status_code}")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
