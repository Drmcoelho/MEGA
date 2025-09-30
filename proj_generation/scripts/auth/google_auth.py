# google_auth.py

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Escopos para a API do Google Drive e outras que possamos usar.
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/generative-language.retriever",
]


def get_google_credentials():
    """Obtém as credenciais do Google, usando um fluxo OAuth 2.0 se necessário.

    Esta função irá procurar por um arquivo `token.json` com as credenciais.
    Se não encontrar ou se as credenciais estiverem expiradas, iniciará um
    fluxo de autenticação local para que o usuário autorize o acesso.

    Returns:
        google.oauth2.credentials.Credentials: As credenciais do usuário.
    """
    creds = None
    # O arquivo token.json armazena os tokens de acesso e de atualização do usuário.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Se não houver credenciais válidas, deixa o usuário fazer login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Idealmente, o token seria atualizado. Para um script de CLI,
            # podemos simplesmente re-autenticar.
            print("Credenciais expiradas. Por favor, autentique-se novamente.")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            print("Nenhuma credencial encontrada. Por favor, autentique-se.")
            # `credentials.json` deve ser baixado do Google Cloud Console
            # e colocado no mesmo diretório.
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Salva as credenciais para a próxima execução
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


if __name__ == "__main__":
    # Exemplo de como usar a função
    print("Obtendo credenciais do Google...")
    credentials = get_google_credentials()
    print("Credenciais obtidas com sucesso!")
    # Aqui você usaria as 'credentials' para inicializar seu cliente de API
    # Ex: service = build('drive', 'v3', credentials=credentials)
