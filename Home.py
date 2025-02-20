import streamlit as st

# Configuração da página
st.set_page_config(page_title="GC ADS", page_icon="📢", layout="centered")

# Inclusão da CDN do Font Awesome (versão 6.3.0)
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css" 
    integrity="sha512-SzlrxWriC3eC9+9e1e2J/3eFOwKpT1h/Sm+dzcF13Zr0fXz7zjG1+1p59Iy8L7ZKMe1ISVb5B0V1XvZJxOk0Og==" 
    crossorigin="anonymous" referrerpolicy="no-referrer" />
    """,
    unsafe_allow_html=True,
)

# CSS customizado para um visual minimalista e responsivo
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
    .icons {
        margin-top: 2rem;
        display: flex;
        gap: 2rem;
        font-size: 2rem;
        justify-content: center;
    }
    .icons i {
        color: #333;
        transition: color 0.3s;
    }
    .icons i:hover {
        color: #0073e6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Container centralizado
st.markdown('<div class="container">', unsafe_allow_html=True)

# Títulos
st.markdown('<h1 class="title">Bem-vindo ao GC ADS</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="sub-title">Seu anúncio no ar em tempo recorde!</h3>', unsafe_allow_html=True)

# Mensagem de orientação
st.markdown('<p style="text-align: center; color: #666;">Utilize o menu ao lado para navegar pelas funcionalidades.</p>', unsafe_allow_html=True)

# Seção de ícones: TikTok, Facebook, Google, IA e Automação
st.markdown(
    """
    <div class="icons">
        <i class="fab fa-tiktok" title="TikTok"></i>
        <i class="fab fa-facebook" title="Facebook"></i>
        <i class="fab fa-google" title="Google"></i>
        <i class="fas fa-robot" title="Inteligência Artificial"></i>
        <i class="fas fa-cogs" title="Automação"></i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)
