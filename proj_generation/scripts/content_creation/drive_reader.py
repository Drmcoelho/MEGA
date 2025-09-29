# drive_reader.py

from googleapiclient.discovery import build
from proj_generation.scripts.auth.google_auth import get_google_credentials

def read_drive_document(document_id: str) -> str:
    """Lê o conteúdo de um documento do Google Drive. Para fins de teste, usa um ID 'test-id' para retornar um texto de exemplo.

    Args:
        document_id (str): O ID do documento do Google Drive ou 'test-id'.

    Returns:
        str: O conteúdo do documento como texto.
    """
    if document_id == "test-id":
        print("Usando rascunho de exemplo para o teste.")
        return ("**Introdução à Insuficiência Cardíaca (IC) - Rascunho**\n\n"
                "- **Definição:** O que é IC? Síndrome clínica complexa. Coração não consegue bombear sangue suficiente.\n"
                "- **Classificação:** IC com Fração de Ejeção Reduzida (ICFEr) vs. Preservada (ICFEp). Estágios A, B, C, D da AHA/ACC.\n"
                "- **Diagnóstico:** Sinais e sintomas (dispneia, edema). Exames: peptídeos natriuréticos (BNP), ecocardiograma.\n"
                "- **Tratamento (ICFEr):** Pilares: IECA/BRA/ARNI, betabloqueadores, antagonistas mineralocorticoides, iSGLT2. Diuréticos para congestão.")

    try:
        creds = get_google_credentials()
        service = build('docs', 'v1', credentials=creds)

        # Obtém o documento
        document = service.documents().get(documentId=document_id).execute()

        # Extrai o texto do corpo do documento
        content = document.get('body').get('content')
        text = ''
        for value in content:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += elem.get('textRun', {}).get('content', '')
        
        return text

    except Exception as e:
        return f"Erro ao ler o documento do Google Drive: {e}"

if __name__ == '__main__':
    # Exemplo de uso: Substitua pelo ID de um documento real para testar
    # O ID pode ser extraído da URL do documento.
    # Ex: https://docs.google.com/document/d/DOCUMENT_ID/edit
    TEST_DOC_ID = '1_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_xxxxxxxx_xx'
    print(f"Lendo o documento do Google Drive com ID: {TEST_DOC_ID}")
    
    # Nota: A execução deste teste exigirá um `credentials.json` válido
    # e um fluxo de autenticação bem-sucedido.
    document_content = read_drive_document(TEST_DOC_ID)
    
    print("\n--- Conteúdo do Documento ---")
    print(document_content)
    print("\n-----------------------------")
