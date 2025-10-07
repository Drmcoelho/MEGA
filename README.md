# MEGA

Medical Education with Generative AI - Plataforma educacional médica com IA generativa.

## Estrutura do Projeto

- **apps/web**: Interface web Next.js
- **content/**: Conteúdo educacional (módulos, lições, quizzes)
- **packages/**: Pacotes Python reutilizáveis
- **scripts/**: Scripts de automação e validação

## Validação de Manifests

Este projeto valida automaticamente os manifestos dos módulos para garantir consistência e qualidade.

### Schema do Manifest

Cada módulo em `content/modules/` deve ter um arquivo `manifest.yaml` com:

**Campos obrigatórios:**
- `id`: Identificador único (kebab-case)
- `title`: Título do módulo

**Campos opcionais:**
- `version`: Versão semântica (padrão: "0.1.0")
- `objectives`: Lista de objetivos de aprendizagem
- `subskills`: Lista de habilidades específicas
- `prerequisites`: Lista de módulos pré-requisitos
- `estimated_time_hours`: Tempo estimado em horas
- `disclaimer`: Aviso legal/educacional

Consulte `content/README.md` para mais detalhes e exemplos.

### Validação Local

Para validar os manifestos localmente antes de fazer commit:

```bash
# Instalar dependências
pip install -r requirements-dev.txt

# Executar validação
python3 scripts/validate_manifests.py
```

### CI/CD

A validação é executada automaticamente no CI através de:

```bash
bash scripts/quality.sh
```

Isso garante que todos os manifestos estejam válidos antes de merge.

### Testes

Para executar os testes de validação:

```bash
pytest tests/test_manifest_validation.py -v
```

## Desenvolvimento

Consulte a documentação específica de cada pacote para instruções de desenvolvimento.