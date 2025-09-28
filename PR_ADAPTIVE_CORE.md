# Adaptive Core (json/sqlite) + Unified Config

## Conteúdo
- mega.config.yaml (adaptive)
- mega-common-utils (config + logging)
- Engine (scheduler, storage JSON/SQLite, engine, erros)
- CLI: mega adaptive rate|mastery|due|snapshot
- Teste básico

## Teste rápido
pip install -e packages/common-utils -e packages/adaptive-engine -e packages/cli
mega adaptive rate demo 2
mega adaptive snapshot

## Próximos
Multi-agent case generator, PDF ingestion, embeddings, lint & typing
