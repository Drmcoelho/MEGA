from .base import Agent

class FailSafeAgent(Agent):
    role = "failsafe"

    def act(self, answer: str):
        # Placeholder de moderação
        risky = any(k in answer.lower() for k in ["diagnóstico definitivo", "dose exata", "prescreva"])
        return {"moderated": risky, "safe": not risky}