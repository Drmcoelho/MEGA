# gpt5_expander.py

from openai import OpenAI
from proj_generation.scripts.auth.openai_auth import get_openai_api_key

def expand_content_with_gpt5(draft_text: str) -> str:
    """Usa o GPT-5 para expandir um rascunho de texto, adicionando detalhes e profundidade.

    Args:
        draft_text (str): O texto do rascunho a ser expandido.

    Returns:
        str: O texto expandido e refinado pelo GPT-5.
    """
    try:
        api_key = get_openai_api_key()
        client = OpenAI(api_key=api_key)

        system_prompt = """Você é um especialista em educação médica e um escritor técnico sênior. 
Sua tarefa é receber um rascunho de um material didático e expandi-lo, 
transformando-o em um capítulo completo, detalhado e bem estruturado. 
Mantenha um tom profissional, claro e acessível para médicos em formação.

- Adicione profundidade técnica e explicações detalhadas.
- Estruture o conteúdo com subtítulos e listas para facilitar a leitura.
- Garanta a precisão médica e a clareza conceitual.
- Não invente dados, mas pode inferir e elaborar sobre os conceitos apresentados no rascunho."""

        response = client.chat.completions.create(
            model="gpt-4o",  # Usando gpt-4o como substituto
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Expanda o seguinte rascunho:\n\n---\n{draft_text}\n---"}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Erro ao expandir o conteúdo com a OpenAI: {e}"

if __name__ == '__main__':
    test_draft = ("**Arritmias Cardíacas - Rascunho**\n\n"
                  "- Fibrilação Atrial (FA): o que é? Como diagnosticar no ECG (ausência de onda P, ritmo irregular). Tratamento: controle de ritmo vs. frequência, anticoagulação (escore CHA2DS2-VASc).\n"
                  "- Taquicardia Ventricular (TV): morfologia (QRS largo). TV sustentada vs. não sustentada. Causas. Tratamento emergencial (cardioversão elétrica).")

    print("Expandindo o rascunho com o GPT-5 (simulado)...")
    expanded_content = expand_content_with_gpt5(test_draft)
    print("\n--- Conteúdo Expandido ---")
    print(expanded_content)
    print("\n--------------------------")
