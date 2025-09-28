# gemini_reviewer.py

import google.generativeai as genai
from proj_generation.scripts.auth.google_auth import get_google_credentials
import os

def generate_code_suggestions_with_gemini(code_diff: str, gpt5_analysis: str) -> str:
    """Recebe um diff de código e a análise do GPT-5, e usa o Gemini para gerar sugestões.

    Args:
        code_diff (str): O diff original do código.
        gpt5_analysis (str): A análise de alto nível fornecida pelo GPT-5.

    Returns:
        str: Um relatório de code review formatado em Markdown com as sugestões do Gemini.
    """
    try:
        # Para a API do Gemini, a autenticação pode ser feita configurando a API key
        # ou usando as credenciais obtidas via OAuth para outros serviços Google.
        # Por simplicidade aqui, vamos assumir que a API key está configurada como variável de ambiente.
        # Em um cenário real, usaríamos as credenciais de `get_google_credentials` se necessário.
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("A variável de ambiente GEMINI_API_KEY não foi encontrada.")
        
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-1.5-flash')

        system_prompt = ("Você é um desenvolvedor de software pragmático e eficiente. "
                         "Sua tarefa é receber um diff de código e uma análise de um arquiteto sênior (GPT-5). "
                         "Com base na análise, você deve gerar sugestões de código concretas e, se possível, o código corrigido. "
                         "Seu output deve ser um relatório claro e formatado em Markdown, contendo:

""
                         "1.  **Resumo da Análise do Arquiteto:** Um resumo breve do que o GPT-5 apontou.
""
                         "2.  **Pontos de Melhoria e Sugestões:** Para cada ponto levantado pelo arquiteto, apresente uma explicação e a sugestão de código.
""
                         "3.  **Blocos de Código Corrigido:** Mostre o bloco de código como ele deveria ficar após as correções.

""
                         "Seja objetivo e ajude o desenvolvedor a entender exatamente o que precisa ser feito.")

        prompt = f"**Análise do Arquiteto (GPT-5):**
{gpt5_analysis}

**Diff de Código Original:**
```diff
{code_diff}
```

Com base na análise e no diff, gere o relatório de code review com as sugestões de implementação."

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Erro ao gerar sugestões com o Gemini: {e}"

if __name__ == '__main__':
    # Exemplo de um diff e análise para teste
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

    gpt5_analysis_example = ("A função `calculate_sum` agora tem um nome enganoso, pois retorna mais do que apenas a soma. "
                             "Além disso, a modificação na chamada `print` pode levar a erros se o chamador não esperar uma tupla. "
                             "Sugira renomear a função e talvez retornar um objeto mais descritivo, como um dicionário.")

    print("Gerando sugestões de código com o Gemini...")
    suggestions = generate_code_suggestions_with_gemini(test_diff, gpt5_analysis_example)
    print("\n--- Relatório de Code Review do Gemini ---")
    print(suggestions)
    print("\n-----------------------------------------")
