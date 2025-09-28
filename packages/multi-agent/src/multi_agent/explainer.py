from .base import Agent

class ExplainerAgent(Agent):
    role = "explainer"

    def act(self, concept: str, level: str="basico"):
        if level == "basico":
            return f"{concept}: Explicação simples inicial."
        if level == "intermediario":
            return f"{concept}: Detalhes adicionais e contexto clínico."
        return f"{concept}: Discussão aprofundada com nuances avançadas."