# Conteúdo Educacional

Estrutura:
- modules/<modulo>/
  - manifest.yaml
  - lessons/
  - quizzes/
  - cases/ (a partir do MVP2)
  - assets/ (imagens, etc.)

## Schema do Manifest.yaml

Cada módulo deve conter um arquivo `manifest.yaml` que segue o schema abaixo.

### Campos Obrigatórios

- **id** (string): Identificador único do módulo
  - Deve conter apenas caracteres alfanuméricos, hífens (-) ou underscores (_)
  - Exemplo: `ecg-basics`, `arrhythmias-basics`

- **title** (string): Título legível do módulo
  - Exemplo: `ECG Básico`, `Arritmias Básicas`

- **version** (string): Versão semântica do módulo
  - Formato: `MAJOR.MINOR.PATCH` (ex: `0.1.0`, `1.2.3`)
  - Todas as partes devem ser números inteiros

### Campos Opcionais

- **objectives** (array de strings): Objetivos de aprendizado do módulo
  - Exemplo: `["Reconhecer derivações", "Identificar ondas P, QRS, T"]`

- **subskills** (array de strings): Subhabilidades cobertas no módulo
  - Exemplo: `["fundamentos-ecg", "morfologia-basica"]`

- **prerequisites** (array de strings): IDs de módulos que são pré-requisitos
  - Exemplo: `["ecg-basics"]`

- **estimated_time_hours** (número): Tempo estimado para completar em horas
  - Deve ser um número positivo (inteiro ou decimal)
  - Exemplo: `2`, `2.5`, `3.0`

- **disclaimer** (string): Texto de aviso/disclaimer do módulo
  - Exemplo: `"Material educacional, não substitui julgamento clínico."`

### Exemplo Completo

```yaml
id: ecg-basics
title: ECG Básico
version: 0.1.0
objectives:
  - Reconhecer derivações
  - Identificar ondas P, QRS, T
subskills:
  - fundamentos-ecg
  - morfologia-basica
prerequisites: []
estimated_time_hours: 2
disclaimer: Material educacional, não substitui julgamento clínico.
```

### Validação

Para validar os manifests localmente, execute:

```bash
python3 scripts/validate_manifests.py
```

Este script verifica todos os manifests em `content/modules/` e reporta erros de forma clara e acionável.

## Padronização de Markdown

- Frontmatter com: id, title, level, time_minutes, objectives, tags

## Quizzes

- Formato JSON (inicial)
- Campos obrigatórios: id, type, stem, options, answer, rationale, subskills