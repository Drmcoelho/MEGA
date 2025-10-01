# Guia de Início Rápido - MEGA

Este guia ajuda você a começar rapidamente com o projeto MEGA.

## Requisitos

- Python 3.11 ou superior
- Git
- pip

## Setup em 5 Minutos

### 1. Clone o Repositório

```bash
git clone https://github.com/Drmcoelho/MEGA.git
cd MEGA
```

### 2. Verifique a Saúde do Projeto

```bash
bash scripts/health-check.sh
```

Este script valida que tudo está configurado corretamente.

### 3. Configure Variáveis de Ambiente

```bash
cp .env.example .env
# Edite .env com suas API keys
```

**Obtenha suas API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Google Gemini: https://makersuite.google.com/app/apikey

### 4. Instale Dependências

```bash
make install
```

Ou manualmente:
```bash
pip install -r requirements-dev.txt

# Instalar pacotes em modo editável
for pkg in packages/*/; do
  pip install -e "$pkg" || true
done
```

### 5. Valide a Instalação

```bash
make all
```

Isso executa:
- Formatação de código
- Linting
- Testes de segurança
- Testes unitários

## Comandos Úteis

### Desenvolvimento

```bash
# Formatar código
make format

# Executar linters
make lint

# Executar testes
make test

# Checks de segurança
make security

# Todos os checks
make all

# Limpar artefatos
make clean
```

### Git Hooks

Instale pre-commit hooks para validação automática:

```bash
make pre-commit
```

Isso garante que seu código é validado antes de cada commit.

## Estrutura do Projeto

```
MEGA/
├── .github/              # GitHub workflows e templates
│   ├── workflows/        # CI/CD pipelines
│   └── ISSUE_TEMPLATE/   # Templates de issues
├── packages/             # Pacotes Python
│   ├── adaptive-engine/  # Motor de aprendizado adaptativo
│   ├── case-generator/   # Gerador de casos clínicos
│   ├── cli/              # Interface de linha de comando
│   ├── common-utils/     # Utilidades compartilhadas
│   ├── content-engine/   # Engine de conteúdo e PDFs
│   ├── llm-orchestrator/ # Orquestrador de LLMs
│   └── multi-agent/      # Sistema multi-agente
├── docs/                 # Documentação
├── scripts/              # Scripts utilitários
├── Makefile              # Comandos de desenvolvimento
├── pytest.ini            # Configuração de testes
└── pyproject.toml        # Configuração do projeto
```

## Primeiro Desenvolvimento

### 1. Crie uma Branch

```bash
git checkout -b feat/minha-feature
```

### 2. Desenvolva

Edite arquivos, adicione código, etc.

### 3. Teste Localmente

```bash
# Durante o desenvolvimento
make format  # Formatar código
make lint    # Verificar estilo

# Antes de commitar
make all     # Executar todos os checks
```

### 4. Commit e Push

```bash
git add .
git commit -m "feat: minha nova feature"
git push origin feat/minha-feature
```

### 5. Abra um Pull Request

No GitHub, abra um PR usando o template fornecido.

## Problemas Comuns

### ImportError: No module named 'X'

```bash
# Reinstale os pacotes
make install
```

### Testes falhando

```bash
# Verifique dependências
pip install -r requirements-dev.txt

# Execute testes específicos
pytest packages/nome-do-pacote/tests/
```

### Pre-commit hooks falhando

```bash
# Formate o código
make format

# Verifique problemas
make lint
```

## Comandos CLI do MEGA

Após instalação, você pode usar os comandos:

```bash
# Sistema adaptativo
mega-cli adaptive rate --item-id "ecg_001" --rating 2

# Geração de casos
mega-cli case generate --topic "Arritmias" --markdown

# Ingestão de PDFs
mega-cli pdf ingest /path/to/pdfs
```

## Próximos Passos

1. Leia [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes detalhadas
2. Veja [docs/architecture.md](docs/architecture.md) para entender a arquitetura
3. Explore [docs/security.md](docs/security.md) para práticas de segurança
4. Confira [docs/roadmap.md](docs/roadmap.md) para planos futuros

## Obtendo Ajuda

- **Issues**: https://github.com/Drmcoelho/MEGA/issues
- **Discussions**: https://github.com/Drmcoelho/MEGA/discussions
- **Documentação**: [docs/](docs/)

## Recursos Adicionais

### Testes

```bash
# Executar todos os testes
pytest

# Testes com cobertura
pytest --cov=packages --cov-report=html

# Testes específicos
pytest packages/adaptive-engine/tests/

# Testes marcados
pytest -m unit
pytest -m "not slow"
```

### Linting

```bash
# Ruff (rápido)
ruff check packages/

# Flake8 (tradicional)
flake8 packages/

# Black (formatação)
black --check packages/

# isort (imports)
isort --check-only packages/
```

### Segurança

```bash
# Auditar dependências
pip-audit -r requirements-dev.txt

# Detectar secrets
detect-secrets scan

# Bandit (security linter)
bandit -r packages/
```

## Contribuindo

Adoramos contribuições! Veja como:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feat/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'feat: add amazing feature'`)
4. Push para a branch (`git push origin feat/amazing-feature`)
5. Abra um Pull Request

Leia [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

## Licença

Este projeto está licenciado sob a licença MIT - veja [LICENSE-DRAFT.md](LICENSE-DRAFT.md).

---

**Pronto para começar? Execute o health check:**

```bash
bash scripts/health-check.sh
```

**Boa codificação! 🚀**
