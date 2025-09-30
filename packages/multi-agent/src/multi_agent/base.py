from abc import ABC, abstractmethod


class Agent(ABC):
    role: str = "generic"

    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator

    @abstractmethod
    def act(self, **kwargs): ...
