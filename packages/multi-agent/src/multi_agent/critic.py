from .base import Agent

class CriticAgent(Agent):
    role = "critic"

    def act(self, passage: str):
        # Placeholder: heurística simples
        flags = []
        if "sempre" in passage.lower():
            flags.append("Uso de afirmação absoluta ('sempre').")
        return {"flags": flags, "ok": len(flags)==0}