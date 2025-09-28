# Adaptive Core (json/sqlite) + Unified Config

## Conteúdo
- `mega.config.yaml` (seção adaptive)
- Pacote `mega-common-utils` (config + logging)
- Engine adaptativa:
  - Backends: JSON (escrita atômica), SQLite
  - IntervalScheduler configurável
  - Erros tipados (`InvalidRatingError`, `BackendNotSupportedError`)
- CLI: `mega adaptive rate|mastery|due|snapshot`
- Teste básico (`test_engine.py`)

## Teste rápido
```bash
pip install -e packages/common-utils -e packages/adaptive-engine -e packages/cli
mega adaptive rate demo 2
mega adaptive snapshot
```

## Próximos PRs
2. Multi-agent case generator
3. PDF ingestion
4. PDF semantic embeddings
5. Lint & typing