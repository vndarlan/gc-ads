# drive_api.py
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Escopo para acesso somente leitura
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    """
    Autentica com a conta de serviço utilizando as credenciais em secrets.toml.
    """
    service_account_info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

def list_files_in_folder(folder_id):
    """
    Lista todos os arquivos da pasta, SEM FILTRAR por vídeo, 
    para depuração e visualização 'crua'.
    """
    drive_service = get_drive_service()
    # Removemos o filtro de 'mimeType contains "video/"' para depuração
    query = f"'{folder_id}' in parents"
    results = drive_service.files().list(
        q=query, 
        pageSize=100,
        fields="files(id, name, mimeType)"
    ).execute()
    
    files = results.get('files', [])
    return files
