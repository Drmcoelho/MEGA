class MultiLLMOrchestrator:
    """Stub de orquestrador multi-LLM.

    Futuro: roteamento dinâmico baseado em custo, latência e qualidade.
    """

    def __init__(self, providers=None):
        self.providers = providers or []

    def generate(self, prompt: str) -> str:
        # Placeholder local
        return f"[stub-response] {prompt[:40]}..."
