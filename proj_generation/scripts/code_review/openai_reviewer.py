# openai_reviewer.py

from openai import OpenAI
from proj_generation.scripts.auth.openai_auth import get_openai_api_key

def analyze_code_with_gpt5(code_diff: str) -> str:
    """Envia um diff de código para o GPT-5 e retorna uma análise de alto nível.

    Args:
        code_diff (str): Uma string contendo o diff das mudanças de código.

    Returns:
        str: A análise gerada pelo GPT-5.
    """
    try:
        api_key = get_openai_api_key()
        client = OpenAI(api_key=api_key)

        system_prompt = """Você é um arquiteto de software sênior e especialista em code review. 
Sua tarefa é analisar o seguinte diff de código e fornecer um feedback de alto nível. 
Concentre-se em:

- **Design e Arquitetura:** A mudança melhora ou prejudica a arquitetura do sistema? Há um padrão de design mais adequado?
- **Boas Práticas e Legibilidade:** O código está claro, bem documentado e segue as melhores práticas da linguagem?
- **Lógica Complexa e Efeitos Colaterais:** Há alguma falha lógica sutil, condição de corrida ou efeito colateral inesperado?
- **Segurança:** A mudança introduz alguma vulnerabilidade de segurança?

Seu feedback deve ser conciso e direto ao ponto, servindo como um guia para um desenvolvedor júnior (que será outro LLM) fazer as correções.
Não sugira o código corrigido, apenas aponte os problemas e a direção para a solução."""

        response = client.chat.completions.create(
            model="gpt-4o",  # Usando gpt-4o como um substituto para o futuro GPT-5
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analise o seguinte diff:\n\n```diff\n{code_diff}\n```"}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Erro ao analisar o código com a OpenAI: {e}"

if __name__ == '__main__':
    # Exemplo de um diff de código para teste
    test_diff = """
    --- a/main.py
    +++ b/main.py
    @@ -1,5 +1,6 @@
     def calculate_sum(a, b):
-    return a + b
+    # Esta função agora retorna a soma e a média
+    return a + b, (a + b) / 2

     result = calculate_sum(10, 5)
-    print(f"A soma é: {result}")
+    print(f"A soma é: {result[0]}, e a média é: {result[1]}")
    """

    print("Analisando o código com o GPT-5 (simulado)...")
    analysis = analyze_code_with_gpt5(test_diff)
    print("\n--- Análise do GPT-5 ---")
    print(analysis)
    print("\n-------------------------")
