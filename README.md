# MEGA - Medical Education with Generative AI

[![CI/CD Pipeline](https://github.com/Drmcoelho/MEGA/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/Drmcoelho/MEGA/actions/workflows/ci.yml)
[![CodeQL](https://github.com/Drmcoelho/MEGA/workflows/CodeQL%20Security%20Analysis/badge.svg)](https://github.com/Drmcoelho/MEGA/actions/workflows/codeql.yml)
[![Security](https://github.com/Drmcoelho/MEGA/workflows/Secret%20Scanning/badge.svg)](https://github.com/Drmcoelho/MEGA/actions/workflows/secrets.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE-DRAFT.md)

Plataforma educacional médica potencializada por IA generativa, focada em aprendizado adaptativo e personalizado.

## 🎯 Características

- **Motor Adaptativo**: Sistema de repetição espaçada com algoritmo de maestria
- **Multi-Agente**: Orquestração de LLMs para tutoria, crítica e explicações
- **Geração de Casos Clínicos**: Criação automatizada de cenários educacionais
- **Ingestão de PDFs**: Indexação e busca em materiais educacionais
- **CLI Robusta**: Interface de linha de comando para todas as funcionalidades
- **APIs RESTful**: Endpoints para integração com outras aplicações

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11 ou superior
- Node.js 18+ (para componentes web)
- pnpm

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Drmcoelho/MEGA.git
cd MEGA

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas API keys

# Instale dependências
pip install -r requirements-dev.txt

# Instale pacotes em modo editável
find packages -name "pyproject.toml" -exec dirname {} \; | while read pkg; do
  pip install -e "$pkg"
done
```

### Uso Básico

```bash
# Execute testes
pytest

# Qualidade de código
./scripts/quality.sh

# CLI
mega-cli adaptive rate --item-id "ecg_001" --rating 2
mega-cli case generate --topic "Arritmias" --markdown
```

## 📚 Documentação

- [Arquitetura](docs/architecture.md)
- [Segurança](docs/security.md)
- [Guia de Contribuição](CONTRIBUTING.md)
- [Política de Segurança](SECURITY.md)
- [Roadmap](docs/roadmap.md)

## 🛡️ Segurança

Este projeto implementa múltiplas camadas de segurança:

- **SAST**: CodeQL para análise estática
- **Auditoria de Dependências**: Dependabot automático
- **Secret Scanning**: TruffleHog + Gitleaks
- **Vulnerability Scanning**: Trivy
- **Pre-commit Hooks**: Validações antes de commit

Veja [SECURITY.md](SECURITY.md) para detalhes sobre como reportar vulnerabilidades.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia nosso [Guia de Contribuição](CONTRIBUTING.md) antes de enviar PRs.

### Processo Rápido

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feat/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'feat: add amazing feature'`)
4. Push para a branch (`git push origin feat/amazing-feature`)
5. Abra um Pull Request

## 📊 Status do Projeto

| Componente | Status | Cobertura |
|------------|--------|-----------|
| Adaptive Engine | ✅ | 80%+ |
| Case Generator | ✅ | 75%+ |
| Content Engine | 🚧 | 60%+ |
| Multi-Agent | ✅ | 70%+ |
| Web App | 🚧 | N/A |

## 📝 Licença

Este projeto está sob a licença MIT. Veja [LICENSE-DRAFT.md](LICENSE-DRAFT.md) para mais detalhes.

## 👥 Autores

- **Dr. Coelho** - *Criador e Mantenedor Principal* - [@Drmcoelho](https://github.com/Drmcoelho)

## 🙏 Agradecimentos

- OpenAI e Google pelos modelos de IA
- Comunidade open source
- Contribuidores do projeto