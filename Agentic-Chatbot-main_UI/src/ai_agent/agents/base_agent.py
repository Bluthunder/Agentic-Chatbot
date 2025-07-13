from abc import ABC, abstractmethod
from ..tools.base_llm import BaseLLM

class Agent(ABC):
    def __init__(self, name: str, llm: BaseLLM):
        self.name = name
        self.llm = llm

    @abstractmethod
    def run(self, state) -> object:
        """Process input state and return updated state"""
        pass
