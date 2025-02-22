# pages/2_🚀_Criar_Anúncio.py
import streamlit as st
import requests
import sys
import os
import datetime

# Configuração de imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_utils import fetch_data

WEBHOOK_URL = "https://primary-production-7d92.up.railway.app/webhook-test/f708e609-9e8b-4940-9cec-55c8cdceb2f7"

def app():
    st.title("📢 Criar Nova Campanha de Anúncios")
    
    # [Restante do código mantido igual até a seção de público-alvo...]

def configurar_anuncio(df, selected_page):
    # [...] Código anterior mantido

        # Seção 3: Configuração do Público-Alvo (CORRIGIDA)
        with st.expander("👥 Configurações de Público", expanded=True):
            st.markdown("**Localizações Alvo**")
            paises = st.multiselect(
                "Selecione países:",
                ["Brasil", "Argentina", "Chile", "Portugal", "México"],
                default=["Brasil"]
            )
            
            col_idade, col_genero = st.columns(2)
            
            # Coluna Idade (CORREÇÃO AQUI)
            with col_idade:
                idade_min, idade_max = st.slider(
                    "Faixa Etária*",
                    18, 65, (25, 55)  # Fechamento correto do parêntese
                )
            
            # Coluna Gênero
            with col_genero:
                genero = st.radio(
                    "Gênero*",
                    ["Ambos", "Homens", "Mulheres"],
                    horizontal=True
                )

            interesses = st.text_input(
                "Interesses (opcional)",
                placeholder="Ex: marketing digital, e-commerce"
            )

    # [Restante do código mantido igual...]

# [...] Funções posteriores mantidas

if __name__ == "__main__":
    app()