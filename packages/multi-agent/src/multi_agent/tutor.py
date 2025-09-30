from .base import Agent


class TutorAgent(Agent):
    role = "tutor"

    def act(self, topic: str):
        return {
            "plan": [
                f"Objetivo principal: Introduzir {topic}",
                "Passo 1: Avaliar conhecimento prévio",
                "Passo 2: Apresentar conceitos nucleares",
                "Passo 3: Quiz diagnóstico",
            ]
        }
