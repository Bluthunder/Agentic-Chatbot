from abc import ABC, abstractmethod
from ai_agent.tools.base_llm import BaseLLM
from src.ai_agent.state.conversation_state import ConversationState

class Agent(ABC):
    def __init__(self, name: str, llm: BaseLLM):
        self.name = name
        self.llm = llm

    @abstractmethod
    async def run(self, state: ConversationState) -> ConversationState:
        """Process input and return response"""
        pass
