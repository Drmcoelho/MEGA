# MEGA

Plataforma modular de educação médica com motor adaptativo, geração de casos clínicos e funcionalidades avançadas de aprendizado.

## CI/CD Pipeline

Este projeto implementa um pipeline de CI/CD completo com GitHub Actions que executa automaticamente em pushes e pull requests.

### Workflows Disponíveis

#### 1. CI/CD Principal (`.github/workflows/ci.yml`)
- **Testes Python**: Executa em Python 3.11 com coverage reports
- **Testes Node.js**: Executa em Node 18 e 20 
- **Build**: Compila aplicação Next.js
- **Lint**: Verifica formatação com Black, isort, flake8 e TypeScript
- **Integração**: Executa scripts de qualidade existentes

#### 2. Code Review (`.github/workflows/code_review.yml`)
- Review automático de código com IA (GPT-5 + Gemini)
- Análise de alto nível e sugestões concretas
- Comentários automáticos em Pull Requests

### Cache e Otimizações

O pipeline utiliza cache para otimizar tempos de build:
- **Python**: Cache de dependências pip baseado em `requirements-dev.txt`
- **Node.js**: Cache do pnpm store e node_modules baseado em `pnpm-lock.yaml`

### Artefatos Gerados

- **Coverage Reports**: Relatórios de cobertura HTML e XML para Python
- **Build Artifacts**: Build da aplicação Next.js
- **Logs**: Logs detalhados de todos os jobs

## Desenvolvimento

### Pré-requisitos

- Python 3.11+
- Node.js 18+ ou 20+
- pnpm (gerenciador de pacotes)

### Instalação

```bash
# Instalar dependências Python
pip install -r requirements-dev.txt

# Instalar dependências Node.js
pnpm install

# Instalar pacotes Python em modo editable
find packages -name "pyproject.toml" -execdir pip install -e . \;
```

### Testes Locais

```bash
# Testes Python com coverage
pytest packages/ --cov=packages --cov-report=html

# Testes Node.js
cd apps/web && pnpm test

# Build da aplicação
cd apps/web && pnpm build

# Executar scripts de qualidade
./scripts/quality.sh
./scripts/run_all_tests.sh
```

### Linting e Formatação

```bash
# Python
black packages/ proj_generation/
isort packages/ proj_generation/
flake8 packages/ proj_generation/

# TypeScript
cd apps/web && npx tsc --noEmit
```

## Deploy

### Ambientes Suportados

O pipeline CI/CD está preparado para expansão para diferentes ambientes:

#### Desenvolvimento
- **Trigger**: Push para branch `develop`
- **Deploy**: Automático após sucesso nos testes
- **Ambiente**: Desenvolvimento/staging

#### Produção
- **Trigger**: Push para branch `main`
- **Deploy**: Manual ou automático após aprovação
- **Ambiente**: Produção

### Expansão para Deploy

Para adicionar etapas de deploy ao pipeline, adicione os seguintes jobs ao arquivo `.github/workflows/ci.yml`:

```yaml
# Exemplo de job de deploy para desenvolvimento
deploy-dev:
  runs-on: ubuntu-latest
  needs: [test-python, test-nodejs, lint, integration]
  if: github.ref == 'refs/heads/develop'
  environment: development
  
  steps:
  - name: Deploy to Development
    run: |
      # Comandos de deploy para desenvolvimento
      echo "Deploying to development environment..."
      
# Exemplo de job de deploy para produção  
deploy-prod:
  runs-on: ubuntu-latest
  needs: [test-python, test-nodejs, lint, integration]
  if: github.ref == 'refs/heads/main'
  environment: production
  
  steps:
  - name: Deploy to Production
    run: |
      # Comandos de deploy para produção
      echo "Deploying to production environment..."
```

### Variáveis de Ambiente para Deploy

Configure as seguintes secrets no GitHub:

- `DEPLOY_TOKEN`: Token de acesso para deploy
- `AWS_ACCESS_KEY_ID`: (se usando AWS)
- `AWS_SECRET_ACCESS_KEY`: (se usando AWS)
- `DOCKER_REGISTRY_URL`: URL do registry Docker
- `PRODUCTION_URL`: URL de produção para verificações

### Estratégias de Deploy Recomendadas

1. **Blue-Green Deployment**: Deploy alternado entre dois ambientes
2. **Rolling Updates**: Atualização gradual de instâncias
3. **Canary Releases**: Deploy incremental com verificação de métricas
4. **Feature Flags**: Controle de funcionalidades via flags

## Estrutura do Projeto

```
.
├── .github/workflows/          # Workflows GitHub Actions
├── apps/web/                   # Aplicação Next.js
├── packages/                   # Pacotes Python modulares
├── proj_generation/            # Ferramentas de geração e automação
├── scripts/                    # Scripts de build e qualidade
└── content/                    # Conteúdo educacional
```

## Monitoramento e Observabilidade

Para ambientes de produção, considere implementar:

- **Logs centralizados** (ELK Stack, Splunk)
- **Métricas de aplicação** (Prometheus, Grafana)
- **APM** (Application Performance Monitoring)
- **Health checks** automatizados
- **Alertas** baseados em SLA/SLO

## Contribuição

1. Crie uma branch a partir de `develop`
2. Faça suas alterações seguindo os padrões de código
3. Execute os testes localmente
4. Crie um Pull Request
5. Aguarde a aprovação do pipeline CI/CD e code review

O pipeline automaticamente executará todos os testes e verificações de qualidade.