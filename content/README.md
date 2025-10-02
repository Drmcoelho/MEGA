# Conteúdo Educacional

Estrutura:
- modules/<modulo>/
  - manifest.yaml
  - lessons/
  - quizzes/
  - cases/ (a partir do MVP2)
  - assets/ (imagens, etc.)

Padronização de Markdown:
- Frontmatter com: id, title, level, time_minutes, objectives, tags

Quizzes:
- Formato JSON (inicial)
- Campos obrigatórios: id, type, stem, options, answer, rationale, subskills