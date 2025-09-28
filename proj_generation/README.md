# Ferramentas de Geração e Automação do Projeto MEGA

Este diretório contém as ferramentas e automações para o desenvolvimento otimizado do projeto MEGA, com foco na integração de LLMs para tarefas como code review e geração de conteúdo.

## Estrutura

- `.github/workflows/`: Contém os workflows do GitHub Actions.
  - `code_review.yml`: Workflow para disparar o processo de code review duplo em pull requests.
- `scripts/`: Contém os scripts Python que executam a lógica principal.
  - `auth/`: Módulos para lidar com a autenticação nas APIs do Google e da OpenAI.
    - `google_auth.py`: Funções para autenticação com APIs do Google (usando OAuth 2.0).
    - `openai_auth.py`: Funções para carregar e usar a chave da API da OpenAI.
  - `code_review/`: Módulos específicos para a tarefa de code review.
    - `openai_reviewer.py`: Script que envia o código para a API da OpenAI (GPT-5) e processa a análise de alto nível.
    - `gemini_reviewer.py`: Script que recebe a análise do GPT-5, envia para a API do Gemini para gerar sugestões de código e formata a saída.
  - `main.py`: O orquestrador principal que é chamado pelo GitHub Action e coordena o fluxo de code review.

## Fluxo de Code Review Duplo

1.  Um desenvolvedor abre um Pull Request no GitHub.
2.  O workflow `code_review.yml` é acionado.
3.  O job no workflow chama o script `scripts/main.py`.
4.  O `main.py` executa os seguintes passos:
    a.  Obtém os arquivos modificados no PR.
    b.  Usa `openai_reviewer.py` para que o GPT-5 analise as mudanças e retorne um feedback de alto nível.
    c.  Usa `gemini_reviewer.py` para pegar o feedback do GPT-5, gerar sugestões de código concretas e formatar um relatório.
    d.  Posta o relatório final como um comentário no Pull Request.
