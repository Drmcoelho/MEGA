
# MEGA - Monorepo de Ensino e Gamificação Adaptativa

Bem-vindo ao MEGA, um projeto de plataforma de e-learning adaptativo focado em cardiologia e ECG.

## Estrutura do Repositório

Este é um monorepo gerenciado com [pnpm workspaces](https://pnpm.io/workspaces). A estrutura é dividida da seguinte forma:

- `apps/`: Contém as aplicações, como a `web` (frontend em Next.js).
- `packages/`: Módulos e bibliotecas Python compartilhadas (ex: `adaptive-engine`, `llm-orchestrator`).
- `content/`: Conteúdo didático dos módulos de ensino.
- `scripts/`: Scripts de utilidade para o projeto.
- `docs/`: Documentação do projeto.

## Configuração do Ambiente de Desenvolvimento

**Pré-requisitos:**

- [Node.js](https://nodejs.org/) (versão 20 ou superior)
- [pnpm](https://pnpm.io/)
- [Python](https://www.python.org/) (versão 3.11 ou superior)

**Passos para Instalação:**

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd MEGA
    ```

2.  **Instale as dependências do frontend:**
    ```bash
    pnpm install
    ```

3.  **Crie e ative um ambiente virtual Python:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4.  **Instale as dependências do backend:**
    ```bash
    pip install -r requirements-dev.txt
    ```

## Comandos Úteis

### Qualidade de Código e Testes

Para garantir a qualidade e a consistência do código, utilize os seguintes comandos:

- **Verificar todo o projeto (Python e Frontend):**
  O workflow de Integração Contínua (`.github/workflows/ci.yml`) executa todas as verificações automaticamente em cada pull request. Para rodar localmente:

  - **Qualidade e Testes do Python:**
    ```bash
    ./scripts/quality.sh
    ```
  - **Lint do Frontend:**
    ```bash
    pnpm --filter mega-web lint
    ```
  - **Testes do Frontend:**
    ```bash
    pnpm test
    ```

- **Formatação de Código:**
  - **Python:**
    ```bash
    ruff format .
    ```
  - **Frontend:**
    ```bash
    pnpm --filter mega-web format
    ```

### Executar a Aplicação

- **Frontend (Next.js):**
  ```bash
  pnpm --filter mega-web dev
  ```
