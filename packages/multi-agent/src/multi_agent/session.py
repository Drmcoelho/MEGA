from .tutor import TutorAgent
from .critic import CriticAgent
from .explainer import ExplainerAgent
from .failsafe import FailSafeAgent

class MultiAgentSession:
    def __init__(self, orchestrator=None):
        self.tutor = TutorAgent(orchestrator)
        self.critic = CriticAgent(orchestrator)
        self.explainer = ExplainerAgent(orchestrator)
        self.failsafe = FailSafeAgent(orchestrator)

    def run_plan(self, topic: str):
        return self.tutor.act(topic=topic)

    def explain_levels(self, concept: str):
        return {
            "basico": self.explainer.act(concept, "basico"),
            "intermediario": self.explainer.act(concept, "intermediario"),
            "avancado": self.explainer.act(concept, "avancado"),
        }