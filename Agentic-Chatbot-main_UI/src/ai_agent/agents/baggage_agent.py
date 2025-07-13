from .base_agent import Agent
from ..tools.llm_loader import get_llm
from ..state.conversation_state import ConversationState

class BaggageAgent(Agent):
    def __init__(self):
        super().__init__(name="BaggageAgent", llm=get_llm())

    def run(self, state: ConversationState) -> ConversationState:
        """
        Handles baggage-related queries.
        """
        prompt = f"You are a helpful assistant providing baggage information and support.\nUser: {state.user_query}\nAgent:"
        response = self.llm.chat([{"role": "user", "content": prompt}])
        state.agent_response = response
        state.agent_name = "BaggageAgent"
        return state
