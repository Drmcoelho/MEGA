# MEGA

(Conteúdo anterior mantido acima)

## Adaptive API (Robusta)
Endpoints:
- GET /api/adaptive/mastery (snapshot)
- GET /api/adaptive/due
- POST /api/adaptive/rate { itemId, rating }
Erros padronizados: `{ error, details? }`.

## Caso Clínico (Multi-Agente Avançado)
```bash
mega case generate "Arritmia Supraventricular" --markdown
```
Retorna JSON ou Markdown estruturado.

## Ingestão de PDFs (Index + Hash)
```bash
pip install PyPDF2
mega pdf ingest docs/pdfs
curl "/api/search/pdf?q=onda"
```
Armazena índice em `data/pdf_index.json` com hash SHA-256, preview e contagem de páginas.

## Configuração Unificada
Arquivo `mega.config.yaml` controla adaptive, pdf, logging, etc. Variáveis de ambiente podem sobrescrever (ex: MEGA_ADAPTIVE_BACKEND).

## CLI Versão
```bash
mega version
```

## Robustez Adicional
- Storage JSON atômico (write temp + replace)
- Locks (RLock) para thread-safety
- Estratégia de intervalos configurável
- Erros tipados (InvalidRatingError, BackendNotSupportedError)
- Logging centralizado
- Índice de PDFs com hash e metadados