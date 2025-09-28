# Arquitetura

Componentes principais:
- Web (Next.js) – UI de módulos, quizzes, progressão.
- CLI – ingestão, futuras operações de dataset e agentes.
- Content Engine – parser de manifests + lições para abstração única.
- Orquestrador multi-LLM – roteamento entre modelos / papéis.
- Adaptive Engine (futuro) – spaced repetition + mastery.
- Fine-tuning pipeline – scripts leves LoRA.