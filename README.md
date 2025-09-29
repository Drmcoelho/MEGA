# MEGA

**Plataforma Educacional Médica com IA Generativa Adaptativa**

MEGA é um sistema educacional moderno para ensino médico que combina tecnologias avançadas como IA generativa, aprendizagem adaptativa e interfaces web interativas para criar uma experiência de aprendizado personalizada e eficaz.

## 🚀 Funcionalidades Principais

- **Sistema Adaptativo de Aprendizagem**: Engine que ajusta automaticamente o conteúdo baseado no progresso individual
- **Geração de Casos Clínicos com IA**: Criação automática de casos personalizados usando LLMs
- **Interface Web Moderna**: Aplicação Next.js com suporte a múltiplos idiomas
- **CLI Robusta**: Ferramentas de linha de comando para gestão de conteúdo e análises
- **Arquitetura Modular**: Monorepo organizado com pacotes Python e aplicações web

## 🏗️ Estrutura do Projeto

```
mega/
├── apps/
│   └── web/                 # Aplicação Next.js
├── packages/
│   ├── adaptive-engine/     # Sistema de aprendizagem adaptativa
│   ├── case-generator/      # Gerador de casos clínicos
│   ├── cli/                 # Interface de linha de comando
│   ├── content-engine/      # Parser de conteúdo educacional
│   └── ...
├── content/                 # Módulos educacionais
├── docs/                    # Documentação
└── .github/                 # Workflows e automações
```

---

## 📋 Estratégia de Branches & Fluxo de PRs {#branch-strategy}

### Nomenclatura de Branches

**Branches Principais:**
- `main` - Código estável em produção
- `develop` - Integração contínua e próxima release

**Branches de Feature:**
```bash
feature/nome-da-funcionalidade
feat/modulo-casos-clinicos
feat/adaptive-engine-improvements
```

**Branches de Correção:**
```bash
fix/bug-description
hotfix/critical-security-patch
```

**Branches de Documentação:**
```bash
docs/update-readme
docs/api-documentation
```

### Processo de Pull Request

1. **Criar Branch**: Partir sempre de `develop` (ou `main` para hotfixes)
```bash
git checkout develop
git pull origin develop
git checkout -b feature/nova-funcionalidade
```

2. **Desenvolvimento**: Fazer commits atômicos e descritivos
```bash
git add .
git commit -m "feat: adiciona geração automática de ECG cases"
```

3. **Sincronizar**: Manter branch atualizada com base
```bash
git fetch origin
git rebase origin/develop
```

4. **Pull Request**: 
   - Use o template em `docs/PR_TEMPLATE_EXAMPLE.md`
   - Aguarde CI/CD passar
   - Solicite review de pelo menos 1 pessoa
   - Resolva comentários do review

5. **Merge Strategy**:
   - **Squash and Merge** para features pequenas
   - **Merge Commit** para features grandes com histórico relevante
   - **Rebase and Merge** para manter histórico linear

### Comandos Úteis

```bash
# Configurar upstream
git remote add upstream https://github.com/Drmcoelho/MEGA.git

# Sincronizar fork
git fetch upstream
git checkout develop
git merge upstream/develop

# Limpar branches antigas
git branch --merged | grep -v "\*\|main\|develop" | xargs -n 1 git branch -d

# Reset de branch problemática
git checkout develop
git branch -D feature/branch-problema
git checkout -b feature/branch-problema
```

---

## ⚙️ GitHub Actions Overview {#github-actions}

### Componentes da Automação

**Workflow** → **Job** → **Step** → **Action** → **Runner**

- **Workflow**: Processo automatizado definido em `.github/workflows/`
- **Job**: Conjunto de steps que rodam em paralelo ou sequencialmente  
- **Step**: Ação individual (comando ou action)
- **Action**: Componente reutilizável (marketplace ou custom)
- **Runner**: Ambiente de execução (ubuntu-latest, windows, etc.)

### Workflows Atuais

#### 1. CI Workflow (`.github/workflows/ci.yml`)
```yaml
Triggers: push (main/develop), PR (main), manual
Jobs:
  - changes: Path filtering para otimização
  - python: Lint + Type Check + Tests + Coverage
  - web: ESLint + TypeScript + Build + Artifacts
  - summary: Relatório consolidado
```

**Caching Strategy:**
- Python: `~/.cache/pip` + requirements hash
- Node: `~/.pnpm-store` + pnpm-lock.yaml hash

#### 2. Release Workflow (`.github/workflows/release.yml`)
```yaml
Triggers: tags v*.*.*, manual dispatch
Features:
  - Build Python packages (wheel/sdist)
  - Build Next.js production
  - Generate release notes
  - Upload artifacts to GitHub Releases
```

#### 3. Security Workflow (`.github/workflows/security.yml`)
```yaml
Status: Commented/Disabled (ready to enable)
Features:
  - CodeQL analysis (JavaScript + Python)
  - Dependency review
  - Scheduled weekly scans
```

### Composite Actions

**Setup Environment** (`.github/actions/setup-env/`)
- Python 3.11 + pip cache
- Node 20 + pnpm
- Cache optimization
- Cross-platform support

### Marketplace Actions Recomendadas

| Categoria | Action | Uso |
|-----------|--------|-----|
| **Core** | `actions/checkout@v4` | Checkout do código |
| **Core** | `actions/setup-python@v5` | Setup Python + cache |
| **Core** | `actions/setup-node@v4` | Setup Node.js + cache |
| **Node** | `pnpm/action-setup@v3` | Setup pnpm |
| **Filtering** | `dorny/paths-filter@v3` | Detectar mudanças |
| **Artifacts** | `actions/upload-artifact@v4` | Upload de artifacts |
| **Releases** | `ncipollo/release-action@v1` | Criação de releases |
| **Security** | `github/codeql-action@v3` | Análise de código |

### Roadmap de Automação

**Fase 1** ✅ - **Fundação CI/CD**
- [x] CI workflow com path filtering
- [x] Composite action para setup
- [x] Release automation básica

**Fase 2** 🔄 - **Qualidade & Segurança**
- [ ] Dependabot configuration
- [ ] CodeQL activation  
- [ ] E2E testing integration
- [ ] Performance monitoring

**Fase 3** 📋 - **Deploy & Environments**
- [ ] Staging environment deployment
- [ ] Production deployment with approvals
- [ ] Environment-specific configurations
- [ ] Rollback strategies

**Fase 4** 📋 - **Avançado**
- [ ] Multi-environment promotion
- [ ] Automated changelog generation
- [ ] Package publishing to PyPI/npm
- [ ] Integration with external monitoring

**Fase 5** 📋 - **DevOps Maturity**
- [ ] Infrastructure as Code (Terraform)
- [ ] Observability dashboard
- [ ] Advanced security scanning
- [ ] Cost optimization automation

---

## ✅ Checklist de Funcionalidades GitHub {#github-features}

### Core Repository Features

| Funcionalidade | Status | Configuração | Notas |
|----------------|--------|--------------|-------|
| **Issues** | ✅ Ativo | Labels, templates | Sistema de bug reports e features |
| **Pull Requests** | ✅ Ativo | Templates, reviews | Workflow de contribuição |
| **Branch Protection** | ⚠️ Básica | Requires PR, 1 review | Configurar para main/develop |
| **GitHub Actions** | ✅ Ativo | CI/CD, Release | Workflows implementados |
| **GitHub Projects** | 📋 A configurar | Kanban boards | Gestão de projetos |
| **Discussions** | 📋 A avaliar | Community forum | Discussões da comunidade |

### Package & Distribution

| Funcionalidade | Status | Configuração | Notas |
|----------------|--------|--------------|-------|
| **GitHub Packages** | 📋 A configurar | Registry privado | Para packages internos |
| **Releases** | ✅ Configurado | Automated releases | Workflow implementado |
| **GitHub Pages** | 📋 A configurar | Docs hosting | Para documentação |

### APIs & Integrations

| Funcionalidade | Status | Configuração | Notas |
|----------------|--------|--------------|-------|
| **GitHub API** | ✅ Disponível | Via workflows | Integração existing |
| **Webhooks** | 📋 A configurar | External integration | Se necessário |
| **GitHub CLI** | ✅ Disponível | `gh` commands | Para automação local |
| **REST API** | ✅ Disponível | Repository access | Acesso programático |
| **GraphQL API** | ✅ Disponível | Advanced queries | Queries complexas |

### Security & Compliance

| Funcionalidade | Status | Configuração | Notas |
|----------------|--------|--------------|-------|
| **Dependabot** | 📋 A configurar | `.github/dependabot.yml` | Atualizações automáticas |
| **Code Scanning** | 📋 Preparado | CodeQL workflow ready | Ativar quando necessário |
| **Secret Scanning** | ⚠️ GitHub detecta | Automatic detection | Monitorar alerts |
| **Security Advisories** | ✅ Disponível | Private disclosure | Para vulnerabilidades |
| **Security Policies** | 📋 A criar | SECURITY.md | Guidelines de security |

### Observability & Analytics

| Funcionalidade | Status | Configuração | Notas |
|----------------|--------|--------------|-------|
| **Insights** | ✅ Ativo | Repository analytics | Métricas built-in |
| **Traffic** | ✅ Ativo | Views, clones | Analytics de tráfego |
| **Dependency Graph** | ✅ Ativo | Auto-generated | Visualização deps |
| **Network Graph** | ✅ Ativo | Branch visualization | Histórico visual |

### Legenda de Status
- ✅ **Ativo/Configurado**: Funcionalidade em uso
- ⚠️ **Básico**: Configuração inicial, pode ser melhorada
- 📋 **A configurar**: Não configurado, recomendado para futuro
- ❌ **Não aplicável**: Não relevante para este projeto

---

## 🛠️ Desenvolvimento Local

### Pré-requisitos

- **Python 3.11+**
- **Node.js 20+**
- **pnpm** (instalado automaticamente)

### Setup Inicial

```bash
# 1. Clonar repositório
git clone https://github.com/Drmcoelho/MEGA.git
cd MEGA

# 2. Instalar dependências Python
pip install -r requirements-dev.txt

# 3. Instalar dependências Node
pnpm install

# 4. Instalar pacotes Python locais
pip install -e packages/cli/
pip install -e packages/common-utils/

# 5. Configurar ambiente web
cd apps/web
pnpm install
pnpm dev  # Inicia servidor de desenvolvimento
```

### Comandos de Desenvolvimento

```bash
# Testes
pnpm test          # Tests frontend
pytest packages/   # Tests Python

# Build
pnpm build         # Build web app
python -m build    # Build Python packages

# Linting
ruff check packages/     # Python linting
eslint apps/web/         # JavaScript/TypeScript linting

# Utilitários
mega --help        # CLI principal
```

---

## 📚 Documentação Adicional

- [Arquitetura do Sistema](docs/architecture.md)
- [Template de Pull Request](docs/PR_TEMPLATE_EXAMPLE.md)
- [Configuração do Projeto](mega.config.yaml)

---

## 🤝 Contribuindo

1. Leia o [template de PR](docs/PR_TEMPLATE_EXAMPLE.md)
2. Siga a [estratégia de branches](#branch-strategy)
3. Execute os testes localmente antes de abrir PR
4. Aguarde review e CI/CD passar

## 📄 Licença

[Licença em definição](LICENSE-DRAFT.md)