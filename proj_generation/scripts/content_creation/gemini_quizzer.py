# gemini_quizzer.py

import google.generativeai as genai
from proj_generation.scripts.auth.google_auth import get_google_credentials


def create_quiz_with_gemini(content_text: str) -> str:
    """Usa o Gemini para criar um quiz (em formato JSON) a partir de um texto didático.

    Args:
        content_text (str): O texto completo do capítulo ou seção.

    Returns:
        str: Uma string contendo um JSON com as perguntas e respostas do quiz.
    """
    try:
        credentials = get_google_credentials()
        genai.configure(credentials=credentials)

        model = genai.GenerativeModel("gemini-1.5-flash")

        system_prompt = """Você é um designer instrucional especializado em criar avaliações de aprendizado para médicos. 
Sua tarefa é receber um texto didático e criar um quiz com 5 perguntas de múltipla escolha. 
O output deve ser um JSON válido, seguindo estritamente a estrutura fornecida.

Estrutura do JSON:
```json
{
  "quiz_title": "Título do Quiz",
  "questions": [
    {
      "question_text": "Texto da Pergunta 1...",
      "options": [
        {\"id\": \"A\", \"text\": \"Texto da Opção A\"},
        {\"id\": \"B\", \"text\": \"Texto da Opção B\"},
        {\"id\": \"C\", \"text\": \"Texto da Opção C\"},
        {\"id\": \"D\", \"text\": \"Texto da Opção D\"}
      ],
      "correct_option_id": "C",
      "explanation": "Uma breve explicação do porquê a opção C está correta."
    }
  ]
}
```"""

        response = model.generate_content(
            f"{system_prompt}\n\nCrie um quiz em JSON a partir do seguinte texto:\n\n---\n{content_text}\n---"
        )

        # O Gemini pode retornar o JSON dentro de um bloco de código, vamos extraí-lo.
        clean_json = response.text.strip().replace("```json", "").replace("```", "")
        return clean_json

    except Exception as e:
        return f"Erro ao criar o quiz com o Gemini: {e}"


if __name__ == "__main__":
    test_content = "A Fibrilação Atrial (FA) é uma taquiarritmia supraventricular caracterizada por atividade atrial caótica e desorganizada, resultando em um ritmo ventricular irregularmente irregular. No ECG, os achados clássicos são a ausência de ondas P discerníveis e a presença de intervalos R-R variáveis. O manejo da FA aguda em pacientes instáveis hemodinamicamente envolve cardioversão elétrica sincronizada imediata. Em pacientes estáveis, a estratégia pode ser controle da frequência cardíaca (com betabloqueadores ou bloqueadores do canal de cálcio) ou controle do ritmo (com antiarrítmicos como amiodarona ou cardioversão). A prevenção de eventos tromboembólicos é crucial, e a decisão de anticoagular é baseada em escores de risco, como o CHA2DS2-VASc, sendo a anticoagulação oral indicada para a maioria dos pacientes com escore ≥ 2."

    print("Gerando quiz com o Gemini (simulado)...")
    quiz_json = create_quiz_with_gemini(test_content)
    print("\n--- Quiz em JSON ---")
    print(quiz_json)
    print("\n--------------------")
