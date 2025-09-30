import os
from typing import Literal, Dict


class LLMOrchestrator:
    def __init__(self, strategy: str = "cost-aware"):
        self.strategy = strategy

    def generate(
        self, prompt: str, intent: Literal["case", "quiz", "explanation"] = "case"
    ) -> Dict:
        """
        Estratégia simples (placeholder):
        1. Tenta modelo local (Mistral via API local/Ollama)
        2. Se precisa refinamento -> chama Gemini (se chave ok)
        3. Ajuste final -> GPT (se disponível)
        """
        draft = self._local_infer(prompt)
        if self._needs_refine(draft):
            refined = self._gemini_refine(draft, intent)
        else:
            refined = draft
        final = self._gpt_polish(refined, intent)
        return {"prompt": prompt, "draft": draft, "refined": refined, "final": final}

    def _local_infer(self, prompt: str) -> str:
        # TODO: chamar ollama/mistral
        return f"[LOCAL_DRAFT]{prompt[:120]}..."

    def _needs_refine(self, text: str) -> bool:
        return True

    def _gemini_refine(self, text: str, intent: str) -> str:
        # TODO: integrar com Gemini
        return f"[GEMINI_REFINED]{text}"

    def _gpt_polish(self, text: str, intent: str) -> str:
        # TODO: integrar com GPT
        return f"[GPT_POLISHED]{text}"
