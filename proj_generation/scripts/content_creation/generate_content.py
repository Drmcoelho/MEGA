# generate_content.py

import sys
import os
import json
from proj_generation.scripts.content_creation.drive_reader import read_drive_document
from proj_generation.scripts.content_creation.gpt5_expander import expand_content_with_gpt5
from proj_generation.scripts.content_creation.gemini_quizzer import create_quiz_with_gemini

def save_content(module_name: str, expanded_content: str, quiz_json: str):
    """Salva o conteúdo gerado em arquivos na estrutura do projeto.

    Args:
        module_name (str): O nome do módulo (ex: 'arritmias').
        expanded_content (str): O conteúdo textual completo em Markdown.
        quiz_json (str): O quiz em formato JSON.
    """
    try:
        # Define o diretório de output baseado no nome do módulo
        output_dir = f"content/modules/{module_name}"
        os.makedirs(output_dir, exist_ok=True)

        # Salva o conteúdo principal
        content_path = os.path.join(output_dir, "content.md")
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(expanded_content)
        print(f"Conteúdo salvo em: {content_path}")

        # Salva o quiz
        quiz_path = os.path.join(output_dir, "quiz.json")
        # Valida e formata o JSON antes de salvar
        try:
            quiz_data = json.loads(quiz_json)
            with open(quiz_path, 'w', encoding='utf-8') as f:
                json.dump(quiz_data, f, ensure_ascii=False, indent=2)
            print(f"Quiz salvo em: {quiz_path}")
        except json.JSONDecodeError:
            print("Erro: O quiz gerado pelo Gemini não é um JSON válido. Salvando como texto.")
            error_path = os.path.join(output_dir, "quiz_error.txt")
            with open(error_path, 'w', encoding='utf-8') as f:
                f.write(quiz_json)
            print(f"Output do quiz (inválido) salvo em: {error_path}")

    except Exception as e:
        print(f"Erro ao salvar os arquivos: {e}")

def main():
    """Função principal que orquestra a geração de conteúdo."""
    if len(sys.argv) < 3:
        print("Uso: python -m proj_generation.scripts.content_creation.generate_content <google_doc_id> <nome_do_modulo>")
        sys.exit(1)

    doc_id = sys.argv[1]
    module_name = sys.argv[2]

    print(f"Iniciando geração de conteúdo para o módulo: '{module_name}' a partir do Google Doc ID: {doc_id}")

    # 1. Ler o rascunho do Google Drive
    print("\n[Passo 1/4] Lendo rascunho do Google Drive...")
    draft_content = read_drive_document(doc_id)
    if draft_content.startswith("Erro"):
        print(draft_content)
        sys.exit(1)
    print("Rascunho lido com sucesso.")

    # 2. Expandir o conteúdo com o GPT-5
    print("\n[Passo 2/4] Expandindo conteúdo com o GPT-5...")
    expanded_content = expand_content_with_gpt5(draft_content)
    if expanded_content.startswith("Erro"):
        print(expanded_content)
        sys.exit(1)
    print("Conteúdo expandido com sucesso.")

    # 3. Criar o quiz com o Gemini
    print("\n[Passo 3/4] Criando quiz com o Gemini...")
    quiz_content = create_quiz_with_gemini(expanded_content)
    if quiz_content.startswith("Erro"):
        print(quiz_content)
        # Mesmo com erro no quiz, podemos salvar o conteúdo principal
        save_content(module_name, expanded_content, "{}")
        sys.exit(1)
    print("Quiz gerado com sucesso.")

    # 4. Salvar os arquivos
    print("\n[Passo 4/4] Salvando arquivos de conteúdo...")
    save_content(module_name, expanded_content, quiz_content)

    print(f"\nProcesso de geração de conteúdo para o módulo '{module_name}' concluído!")

if __name__ == '__main__':
    main()
