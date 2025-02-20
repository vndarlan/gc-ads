import streamlit as st

# Configuração da página
st.set_page_config(page_title="Dashboard", page_icon="🌟", layout="centered")

# CSS customizado para um visual minimalista
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .title {
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #333;
    }
    .sub-title {
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Container centralizado
st.markdown('<div class="container">', unsafe_allow_html=True)

# Exibe o GIF ou imagem (substitua o URL se desejar outro)
gif_url = "https://media.giphy.com/media/3o7TKO32FEGLZEXjyI/giphy.gif"
st.image(gif_url, width=400)

# Títulos
st.markdown('<h1 class="title">Bem-vindo a GC ADS</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="sub-title">Seu anúncio no ar em tempo recorde!</h3>', unsafe_allow_html=True)

# Mensagem de orientação
st.markdown('<p style="text-align: center; color: #666;">Utilize o menu ao lado para navegar pelas funcionalidades.</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
