from abc import ABC, abstractmethod
from ai_agent.tools.base_llm import BaseLLM

class Agent(ABC):
    def __init__(self, name: str, llm: BaseLLM):
        self.name = name
        self.llm = llm

    @abstractmethod
    def run(self, input_text: str) -> str:
        """Process input and return response"""
        pass
