import streamlit as st
from db_utils import create_table_if_not_exists
import sys
import os

# Configuração do path para o VS Code
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    st.set_page_config(
        page_title="GC ADS",
        page_icon="📢",
        layout="wide",  # Alterado para wide para melhor uso do espaço
        initial_sidebar_state="auto"
    )

    # Container principal
    with st.container():
        # Divisão em duas colunas
        col1, col2 = st.columns([2, 1])  # Proporção 2:1 entre as colunas

        with col1:
            # Conteúdo da primeira coluna (apresentação)
            st.title("Agente Facebook")
            st.markdown("""                
                ℹ️ Navegue pelo menu lateral para acessar as diferentes 
                funcionalidades da plataforma.
                """)
            
            # Link para o Google Drive
            st.markdown("ℹ️ Acesso aos Vídeos")
            drive_url = "https://drive.google.com/drive/u/0/folders/1_G2LZe_0gs95XWUVSmxrDK0pCUvdaut9"
            st.markdown(f"""
                Acesse nosso repositório de vídeos clicando no link abaixo:  
                [Acessar Drive de Vídeos]({drive_url})
                """)

        with col2:
            # Conteúdo da segunda coluna (vídeo)
            st.markdown("## Tutorial")
            video_url = "https://www.youtube.com/watch?v=sxTNACldK3Y"  # Substituir pelo link real
            st.video(video_url)  # Streamlit tem suporte nativo para embed de vídeos
            
            # Ou usando iframe para embed mais personalizado
            # st.components.v1.html("""
            # <iframe width="100%" height="315" src="https://www.youtube.com/embed/VIDEO_AQUI" 
            # frameborder="0" allowfullscreen></iframe>
            # """, height=350)

    create_table_if_not_exists()

if __name__ == "__main__":
    main()
