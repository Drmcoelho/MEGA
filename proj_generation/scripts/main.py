# main.py

import os
import sys
from proj_generation.scripts.code_review.openai_reviewer import analyze_code_with_gpt5
from proj_generation.scripts.code_review.gemini_reviewer import generate_code_suggestions_with_gemini

def get_pr_diff():
    """Obtém o diff do Pull Request.

    Em um cenário real no GitHub Actions, usaríamos uma action como `actions/checkout`
    e depois `git diff` para obter as mudanças. Para este exemplo, vamos simular
    lendo o diff de um arquivo ou de uma variável de ambiente.

    Returns:
        str: O diff do PR.
    """
    # Simulação: O diff seria passado como um argumento de linha de comando ou lido de um arquivo.
    if len(sys.argv) > 1:
        diff_file = sys.argv[1]
        if os.path.exists(diff_file):
            with open(diff_file, 'r') as f:
                return f.read()
    
    # Fallback para um diff de exemplo se nenhum arquivo for fornecido
    print("Aviso: Nenhum arquivo de diff fornecido. Usando diff de exemplo.")
    return """
    --- a/example.py
    +++ b/example.py
    @@ -1,3 +1,4 @@
     def old_function(x):
         # Esta função está obsoleta
-    return x * 2
+    # Nova lógica mais complexa
+    return (x * 2) + 1
    """

def post_comment_to_pr(comment: str):
    """Posta um comentário no Pull Request.

    Em um cenário real, usaríamos a API do GitHub para postar o comentário.
    Para este exemplo, vamos apenas imprimir o comentário no console.

    Args:
        comment (str): O comentário a ser postado.
    """
    print("\n--- COMENTÁRIO PARA O PULL REQUEST ---")
    print(comment)
    print("-------------------------------------")
    # Em um uso real:
    # github_token = os.getenv("GITHUB_TOKEN")
    # pr_number = os.getenv("PR_NUMBER")
    # repo_name = os.getenv("GITHUB_REPOSITORY")
    # ... fazer a chamada para a API do GitHub ...

def main():
    """Função principal que orquestra o processo de code review duplo."""
    print("Iniciando processo de Code Review Duplo...")

    # 1. Obter o diff do PR
    print("\n[Passo 1/4] Obtendo o diff do Pull Request...")
    pr_diff = get_pr_diff()
    print("Diff obtido com sucesso.")

    # 2. Análise de alto nível com o GPT-5
    print("\n[Passo 2/4] Enviando para análise do GPT-5 (Arquiteto Sênior)...")
    gpt5_analysis = analyze_code_with_gpt5(pr_diff)
    print("Análise do GPT-5 recebida.")

    # 3. Geração de sugestões com o Gemini
    print("\n[Passo 3/4] Enviando para o Gemini (Desenvolvedor Executor) gerar sugestões...")
    gemini_suggestions = generate_code_suggestions_with_gemini(pr_diff, gpt5_analysis)
    print("Sugestões do Gemini recebidas.")

    # 4. Montar e postar o comentário final
    print("\n[Passo 4/4] Montando e postando o comentário final...")
    final_comment = f"""## Análise de Code Review (IA-Powered) 🤖✨

Olá! Analisei as suas mudanças com a ajuda de um time de IAs.

### Análise do Arquiteto Sênior (GPT-5)

{gpt5_analysis}

---

### Sugestões de Implementação (Gemini)

{gemini_suggestions}

---

*Este comentário foi gerado automaticamente. As sugestões devem ser revisadas por um humano.*"""
    
    post_comment_to_pr(final_comment)
    print("\nProcesso de Code Review Duplo concluído!")

if __name__ == '__main__':
    main()
