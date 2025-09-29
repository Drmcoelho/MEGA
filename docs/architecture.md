
# Arquitetura do Sistema MEGA

O MEGA é projetado como um monorepo modular para facilitar o desenvolvimento e a manutenção de uma plataforma de e-learning adaptativa. A arquitetura é dividida em três áreas principais: Frontend, Backend e Ferramentas de Suporte.

## Diagrama de Componentes

```mermaid
graph TD
    subgraph Frontend
        WebApp[Aplicação Web (Next.js)]
    end

    subgraph Backend Services
        APIServer[API Server (FastAPI)]
        LLM[Orquestrador LLM]
        Adaptive[Motor Adaptativo]
        Content[Motor de Conteúdo]
    end

    subgraph Tooling & Infrastructure
        CLI[CLI de Gerenciamento]
        Finetune[Pipeline de Fine-tuning]
        ContentRepo[Repositório de Conteúdo]
    end

    WebApp --> APIServer
    APIServer --> LLM
    APIServer --> Adaptive
    APIServer --> Content
    CLI --> Content
    CLI --> Finetune
    ContentRepo -- "Ingestão via CLI" --> Content
```

## Componentes Principais

### Frontend

-   **Aplicação Web (`apps/web`):**
    -   **Tecnologia:** Next.js e React.
    -   **Responsabilidade:** Interface do usuário para os alunos, incluindo a visualização dos módulos de ensino, quizzes, e acompanhamento do progresso. Interage com o Backend através de uma API REST.

### Backend

Os serviços de backend são construídos primariamente em Python.

-   **API Server (FastAPI - a ser implementado):**
    -   **Responsabilidade:** Ponto de entrada único para o frontend. Orquestra as chamadas para os outros serviços de backend.

-   **Motor Adaptativo (`packages/adaptive-engine`):
    -   **Responsabilidade:** Gerencia a lógica de aprendizado adaptativo, como Spaced Repetition e o cálculo do nível de maestria do aluno em cada habilidade.

-   **Orquestrador Multi-LLM (`packages/llm-orchestrator`):
    -   **Responsabilidade:** Roteia os prompts para o modelo de linguagem (LLM) mais apropriado, dependendo da tarefa (ex: gerar questões, explicar um conceito).

-   **Motor de Conteúdo (`packages/content-engine`):
    -   **Responsabilidade:** Processa e serve o conteúdo didático (lições, quizzes) a partir dos arquivos de manifesto (`content/`).

### Ferramentas e Infraestrutura (Tooling)

-   **CLI (`packages/cli`):
    -   **Responsabilidade:** Ferramenta de linha de comando para tarefas administrativas, como a ingestão de novo conteúdo para o `Content Engine` ou o disparo de processos de fine-tuning.

-   **Pipeline de Fine-tuning (`models/finetune`):
    -   **Responsabilidade:** Contém os scripts e configurações para o fine-tuning de modelos de linguagem (LLMs) com dados específicos do domínio (ECG, cardiologia).
