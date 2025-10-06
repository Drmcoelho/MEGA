# Segurança e Conformidade no MEGA

Este documento detalha as práticas de segurança, conformidade e governança implementadas no projeto MEGA.

## Índice

- [Visão Geral](#visão-geral)
- [Análise de Segurança (SAST/DAST)](#análise-de-segurança-sastdast)
- [Auditoria de Dependências](#auditoria-de-dependências)
- [Detecção de Secrets](#detecção-de-secrets)
- [Práticas de Desenvolvimento Seguro](#práticas-de-desenvolvimento-seguro)
- [Compliance e Governança](#compliance-e-governança)

## Visão Geral

O projeto MEGA implementa múltiplas camadas de segurança automatizada através de:

- **SAST (Static Application Security Testing)**: CodeQL
- **Auditoria de Dependências**: Dependabot + pip-audit
- **Secret Scanning**: TruffleHog + Gitleaks
- **Vulnerability Scanning**: Trivy
- **Code Quality**: Ruff, Black, isort, mypy

## Análise de Segurança (SAST/DAST)

### CodeQL

CodeQL é executado automaticamente em:
- Todo push para `main` e `develop`
- Todo pull request
- Diariamente às 00:00 UTC

**Configuração**: `.github/workflows/codeql.yml`

**Análises Realizadas**:
- Injeção de código
- Exposição de dados sensíveis
- Vulnerabilidades de autenticação
- Problemas de criptografia
- Path traversal
- XSS e outras vulnerabilidades web

**Consultas Executadas**:
- `security-extended`: Queries avançadas de segurança
- `security-and-quality`: Segurança + qualidade de código

### Trivy Scanner

Trivy verifica vulnerabilidades em:
- Dependências Python
- Dependências JavaScript/Node
- Arquivos de configuração
- IaC (Infrastructure as Code)

**Uso Local**:
```bash
# Instalar Trivy
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# Escanear o projeto
trivy fs --severity HIGH,CRITICAL .
```

## Auditoria de Dependências

### Dependabot

Configurado em `.github/dependabot.yml` para monitorar:

- **Dependências Python** (pip)
- **GitHub Actions**
- **npm/pnpm packages**

**Política de Atualização**:
- Verificação semanal (segunda-feira)
- Até 10 PRs abertos simultâneos para Python/npm
- Até 5 PRs abertos para GitHub Actions
- Prioridade automática para updates de segurança

### pip-audit

Ferramenta para auditoria manual de dependências Python.

**Uso**:
```bash
# Instalar
pip install pip-audit

# Auditar requirements
pip-audit -r requirements-dev.txt

# Auditar ambiente atual
pip-audit

# Gerar relatório JSON
pip-audit --format json --output audit-report.json
```

**Integração CI**: Executado automaticamente no workflow de CI.

## Detecção de Secrets

### TruffleHog

Detecta secrets commitados no histórico git.

**Características**:
- Verifica todo o histórico
- Detecta padrões de API keys, tokens, senhas
- Valida secrets encontrados (quando possível)

**Uso Local**:
```bash
# Instalar
pip install trufflehog

# Escanear repositório
trufflehog git file://. --only-verified

# Escanear desde um commit
trufflehog git file://. --since-commit <commit-sha>
```

### Gitleaks

Alternativa ao TruffleHog com diferentes patterns.

**Uso Local**:
```bash
# Instalar
brew install gitleaks  # macOS
# ou baixar de https://github.com/gitleaks/gitleaks/releases

# Escanear repositório
gitleaks detect --source . --verbose

# Escanear uncommited changes
gitleaks protect --verbose
```

### Pre-commit Hooks

O hook `detect-secrets` previne commits com secrets:

```bash
# Instalar
pip install pre-commit
pre-commit install

# Criar baseline (primeira vez)
detect-secrets scan > .secrets.baseline

# Auditar baseline
detect-secrets audit .secrets.baseline
```

## Práticas de Desenvolvimento Seguro

### 1. Gestão de Secrets

**❌ NUNCA faça isso**:
```python
# ERRADO - Secret hardcoded
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"
```

**✅ Faça isso**:
```python
# CORRETO - Use variáveis de ambiente
import os
API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Com valor padrão seguro
LOG_LEVEL = os.getenv("MEGA_LOG_LEVEL", "INFO")
```

### 2. Validação de Entrada

**❌ NUNCA faça isso**:
```python
# ERRADO - SQL Injection vulnerável
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

**✅ Faça isso**:
```python
# CORRETO - Use prepared statements
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### 3. Logging Seguro

**❌ NUNCA faça isso**:
```python
# ERRADO - Log expõe dados sensíveis
logger.info(f"User login: {username} with password {password}")
logger.debug(f"API Key: {api_key}")
```

**✅ Faça isso**:
```python
# CORRETO - Log sem dados sensíveis
logger.info(f"User login attempt: {username}")
logger.debug("API authentication successful")

# Ou mascare dados sensíveis
def mask_secret(secret: str, visible: int = 4) -> str:
    if len(secret) <= visible:
        return "***"
    return secret[:visible] + "***" + secret[-visible:]

logger.debug(f"Using API key: {mask_secret(api_key)}")
```

### 4. Tratamento de Erros

**❌ NUNCA faça isso**:
```python
# ERRADO - Expõe stack trace completo
@app.route("/api/data")
def get_data():
    return jsonify({"data": process_data()})
```

**✅ Faça isso**:
```python
# CORRETO - Tratamento seguro de erros
@app.route("/api/data")
def get_data():
    try:
        return jsonify({"data": process_data()})
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
```

### 5. Autenticação e Autorização

```python
# Use bibliotecas estabelecidas
from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not validate_api_key(api_key):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route("/api/secure")
@require_api_key
def secure_endpoint():
    return jsonify({"data": "sensitive information"})
```

## Compliance e Governança

### Code Review Obrigatório

- Todo PR requer pelo menos 1 aprovação
- PRs de segurança requerem 2 aprovações
- Maintainers podem fazer merge apenas de seus PRs não-críticos

### Testes de Segurança

Executados automaticamente em CI:

```bash
# Localmente
pytest tests/security/

# Com marcadores específicos
pytest -m security
```

### Checklist de Segurança para PR

Antes de submeter um PR, verifique:

- [ ] Nenhum secret ou credencial commitado
- [ ] Variáveis de ambiente para configurações sensíveis
- [ ] Validação e sanitização de inputs
- [ ] Tratamento apropriado de erros
- [ ] Logs não expõem dados sensíveis
- [ ] Testes de segurança incluídos
- [ ] Dependências auditadas
- [ ] Documentação de segurança atualizada

### Versionamento Semântico Estrito

- **MAJOR** (x.0.0): Breaking changes + revisão de segurança
- **MINOR** (0.x.0): Novas features + auditoria de segurança
- **PATCH** (0.0.x): Bug fixes + verificação de regressão

### Documentação

Toda mudança de segurança deve ser documentada:

- Atualizar `SECURITY.md` se aplicável
- Adicionar entrada em `CHANGELOG.md`
- Documentar novas configurações de segurança
- Atualizar guias de deployment se necessário

## Monitoramento e Resposta

### Alertas Automatizados

GitHub Security Alerts são configurados para:
- Vulnerabilidades em dependências
- Secrets detectados
- Falhas no CodeQL

### Resposta a Incidentes

1. **Detecção**: Alerta automático ou relatório manual
2. **Avaliação**: Severidade e impacto
3. **Contenção**: Medidas imediatas
4. **Correção**: Desenvolvimento e teste de fix
5. **Deployment**: Release de correção
6. **Post-mortem**: Análise e prevenção

### Contatos de Segurança

- GitHub Security Advisories: https://github.com/Drmcoelho/MEGA/security/advisories
- Email: [ADICIONAR EMAIL]

## Recursos Adicionais

### Treinamento

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Python Security](https://python.readthedocs.io/en/stable/library/security_warnings.html)

### Ferramentas

- [Bandit](https://bandit.readthedocs.io/) - Python security linter
- [Safety](https://pyup.io/safety/) - Dependency checker
- [Semgrep](https://semgrep.dev/) - Static analysis

### Standards

- [CWE (Common Weakness Enumeration)](https://cwe.mitre.org/)
- [CVE (Common Vulnerabilities and Exposures)](https://cve.mitre.org/)
- [CVSS (Common Vulnerability Scoring System)](https://www.first.org/cvss/)

## Atualizações

Este documento é revisado trimestralmente e atualizado conforme necessário.

**Última atualização**: 2024-10-01
**Próxima revisão**: 2025-01-01
