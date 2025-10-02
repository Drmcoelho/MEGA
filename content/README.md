# Conteúdo Educacional

Estrutura:
- modules/<modulo>/
  - manifest.yaml
  - lessons/
  - quizzes/
  - cases/ (a partir do MVP2)
  - assets/ (imagens, etc.)

## Manifest Schema

Cada módulo deve ter um arquivo `manifest.yaml` seguindo este esquema:

### Campos Obrigatórios
- `id` (string): Identificador único do módulo em kebab-case (ex: `ecg-basics`)
- `title` (string): Título legível do módulo (ex: `ECG Básico`)

### Campos Opcionais
- `version` (string): Versão semântica (padrão: `"0.1.0"`)
- `objectives` (array de strings): Objetivos de aprendizagem
- `subskills` (array de strings): Habilidades específicas cobertas
- `prerequisites` (array de strings): IDs de módulos pré-requisitos
- `estimated_time_hours` (number): Tempo estimado de conclusão em horas
- `disclaimer` (string): Aviso legal/educacional

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

Para validar os manifestos localmente:
```bash
python3 scripts/validate_manifests.py
```

A validação é executada automaticamente no CI através de `scripts/quality.sh`.

## Padronização de Markdown

Frontmatter com: id, title, level, time_minutes, objectives, tags

## Quizzes

Formato JSON (inicial)
Campos obrigatórios: id, type, stem, options, answer, rationale, subskills