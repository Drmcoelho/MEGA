# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Adicionado

#### Segurança
- Workflow de análise SAST com CodeQL para Python e JavaScript
- Workflow de detecção de secrets com TruffleHog e Gitleaks
- Configuração do Dependabot para auditoria automática de dependências
- Scanning de vulnerabilidades com Trivy
- Pre-commit hooks para validação de código e secrets
- Política de segurança detalhada em SECURITY.md
- Documentação de segurança em docs/security.md

#### Qualidade
- Workflow de CI/CD multi-stage com lint, test, e build
- Configuração de linting com ruff, flake8, black, isort
- Configuração de testes com pytest e coverage
- Configuração de mypy para type checking
- Pre-commit hooks para formatação automática
- Configuração do pytest.ini para testes unificados

#### Automação
- Pipeline de CI/CD automatizado no GitHub Actions
- Cache de dependências para builds mais rápidos
- Execução de testes em múltiplas versões do Python (3.11, 3.12)
- Upload automático de coverage para Codecov
- Build validation automatizado

#### Governança
- Template de Pull Request estruturado
- Templates de Issues (Bug Report, Feature Request, Security)
- Guia de contribuição detalhado (CONTRIBUTING.md)
- Makefile com comandos comuns de desenvolvimento
- Política de versionamento semântico

#### Infraestrutura
- Arquivo .gitignore abrangente
- Configuração do ruff em pyproject.toml
- Configuração de pre-commit hooks
- Estrutura de diretórios .github/workflows

#### Documentação
- README.md atualizado com badges de status
- Documentação de segurança completa
- Guia de contribuição
- Exemplos de uso
- Seção de práticas de desenvolvimento seguro

### Modificado
- requirements-dev.txt: Adicionadas ferramentas de teste, qualidade e segurança
- README.md: Expandido com badges, documentação e guias

## [0.1.0] - YYYY-MM-DD

### Adicionado
- Motor adaptativo com backend JSON e SQLite
- Gerador de casos clínicos multi-agente
- Ingestão e indexação de PDFs
- CLI para operações principais
- APIs REST para adaptive engine e busca de PDFs
- Sistema de logging configurável
- Configuração unificada via mega.config.yaml

[Unreleased]: https://github.com/Drmcoelho/MEGA/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Drmcoelho/MEGA/releases/tag/v0.1.0
