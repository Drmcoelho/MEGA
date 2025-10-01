# Guia de Contribuição

Obrigado por considerar contribuir para o projeto MEGA! 🎉

## Sumário

- [Código de Conduta](#código-de-conduta)
- [Como Posso Contribuir?](#como-posso-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Commits e Pull Requests](#commits-e-pull-requests)

## Código de Conduta

Este projeto adere a um código de conduta. Ao participar, você deve manter um comportamento respeitoso e profissional.

## Como Posso Contribuir?

### Reportando Bugs

- Use o template de issue para bugs
- Descreva o problema claramente
- Inclua passos para reprodução
- Adicione logs e screenshots se relevante

### Sugerindo Melhorias

- Use o template de issue para features
- Explique o caso de uso
- Considere alternativas
- Esteja aberto a discussão

### Contribuindo com Código

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feat/amazing-feature`)
3. Faça commit das mudanças (`git commit -m 'feat: add amazing feature'`)
4. Push para a branch (`git push origin feat/amazing-feature`)
5. Abra um Pull Request

## Configuração do Ambiente

### Pré-requisitos

- Python 3.11 ou superior
- Node.js 18 ou superior (para componentes web)
- pnpm (gerenciador de pacotes)
- git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Drmcoelho/MEGA.git
cd MEGA

# Instale dependências Python
pip install -r requirements-dev.txt

# Instale pacotes do projeto em modo editável
find packages -name "pyproject.toml" -exec dirname {} \; | while read pkg; do
  pip install -e "$pkg"
done

# Instale dependências Node (se aplicável)
pnpm install

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações
```

### Configuração das APIs

Para desenvolvimento local, você precisará de:

- OpenAI API Key: https://platform.openai.com/api-keys
- Google Gemini API Key: https://makersuite.google.com/app/apikey

Adicione ao arquivo `.env`:

```bash
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

## Processo de Desenvolvimento

### 1. Escolha uma Issue

- Procure issues com labels `good first issue` ou `help wanted`
- Comente na issue indicando interesse
- Aguarde atribuição antes de começar

### 2. Crie uma Branch

Use o padrão de nomenclatura:

- `feat/nome-da-feature` - Nova funcionalidade
- `fix/nome-do-bug` - Correção de bug
- `docs/descricao` - Documentação
- `refactor/descricao` - Refatoração
- `test/descricao` - Adição/melhoria de testes

### 3. Desenvolva

- Siga os padrões de código (veja abaixo)
- Escreva testes para novas funcionalidades
- Mantenha commits pequenos e focados
- Execute testes localmente

### 4. Teste

```bash
# Execute todos os testes
pytest

# Execute testes com cobertura
pytest --cov=packages --cov-report=html

# Execute linting
ruff check packages/
black --check packages/
isort --check-only packages/
```

### 5. Abra um Pull Request

- Use o template de PR
- Descreva as mudanças claramente
- Referencie issues relacionadas
- Aguarde revisão

## Padrões de Código

### Python

- Siga PEP 8
- Use type hints quando possível
- Docstrings no formato Google
- Máximo de 120 caracteres por linha

```python
def calculate_mastery(skill_id: str, rating: int) -> dict[str, float]:
    """Calcula o nível de maestria para uma habilidade.

    Args:
        skill_id: Identificador único da habilidade
        rating: Avaliação do usuário (0-2)

    Returns:
        Dicionário com dados de maestria

    Raises:
        ValueError: Se rating não estiver no intervalo válido
    """
    if not 0 <= rating <= 2:
        raise ValueError(f"Rating inválido: {rating}")
    
    # Implementação...
    return {"mastery": 0.0}
```

### Formatação

Use as ferramentas automáticas:

```bash
# Formatar código
black packages/
isort packages/

# Verificar estilo
ruff check packages/
flake8 packages/
```

### JavaScript/TypeScript

- Use ESLint e Prettier
- Siga convenções do Airbnb Style Guide
- Use TypeScript quando possível

## Testes

### Estrutura de Testes

```
packages/
  nome-do-pacote/
    src/
      module.py
    tests/
      test_module.py
```

### Escrevendo Testes

```python
import pytest
from nome_do_pacote import module

def test_funcao_basica():
    """Testa comportamento básico."""
    result = module.funcao(input_data)
    assert result == expected

def test_funcao_com_erro():
    """Testa tratamento de erro."""
    with pytest.raises(ValueError):
        module.funcao(invalid_data)

@pytest.mark.slow
def test_operacao_demorada():
    """Testa operação que demora."""
    # Teste longo...
```

### Executando Testes

```bash
# Todos os testes
pytest

# Testes específicos
pytest packages/adaptive-engine/tests/

# Testes com marcadores
pytest -m "not slow"

# Com cobertura
pytest --cov=packages --cov-report=term-missing
```

### Cobertura de Código

- Alvo: 80% de cobertura mínima
- Priorize testes de lógica crítica
- Use `# pragma: no cover` com justificativa

## Commits e Pull Requests

### Mensagens de Commit

Siga o padrão Conventional Commits:

```
tipo(escopo): descrição curta

Descrição mais detalhada se necessário.

Fixes #123
```

Tipos:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de lógica)
- `refactor`: Refatoração
- `test`: Adição/melhoria de testes
- `chore`: Tarefas de manutenção
- `perf`: Melhoria de performance
- `ci`: Mudanças em CI/CD

Exemplos:

```bash
feat(adaptive): add mastery calculation algorithm
fix(pdf): resolve unicode encoding error
docs(readme): update installation instructions
test(case-gen): add edge case tests
```

### Pull Requests

#### Checklist

- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Testes passam localmente
- [ ] Documentação foi atualizada
- [ ] Commit messages seguem o padrão
- [ ] Branch está atualizada com main/develop
- [ ] Nenhum secret ou credencial foi commitado

#### Tamanho

- Mantenha PRs pequenos e focados
- Um PR = uma feature/fix
- PRs grandes devem ser divididos

#### Revisão

- Seja receptivo a feedback
- Responda comentários prontamente
- Faça mudanças solicitadas
- Marque conversas como resolvidas

## Processo de Revisão

### Para Revisores

- Seja construtivo e respeitoso
- Foque em código, não em pessoas
- Sugira melhorias claras
- Aprove quando satisfeito

### Para Autores

- Não leve críticas pessoalmente
- Peça esclarecimentos se necessário
- Faça mudanças solicitadas
- Agradeça pelo tempo do revisor

## Lançamento de Versões

Seguimos Versionamento Semântico (SemVer):

- **MAJOR**: Mudanças incompatíveis
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções compatíveis

Exemplo: `0.1.0` → `0.2.0` → `1.0.0`

## Ferramentas Recomendadas

### IDE/Editor

- VSCode com extensões:
  - Python
  - Pylance
  - Black Formatter
  - isort
  - Ruff

### Linha de Comando

```bash
# Pre-commit hooks (recomendado)
pip install pre-commit
pre-commit install

# Executar manualmente
pre-commit run --all-files
```

## Dúvidas?

- Abra uma issue com label `question`
- Participe das discussões
- Consulte a documentação em `/docs`

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.

---

**Obrigado por contribuir para o MEGA! 🚀**
