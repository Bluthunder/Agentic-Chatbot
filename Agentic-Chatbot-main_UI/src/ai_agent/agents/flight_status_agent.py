from .base_agent import Agent
from ..tools.llm_loader import get_llm
from ..state.conversation_state import ConversationState

class FlightStatusAgent(Agent):
    def __init__(self):
        super().__init__(name="FlightStatusAgent", llm=get_llm())

    def run(self, state: ConversationState) -> ConversationState:
        prompt = f"You are a helpful assistant providing flight status updates.\nUser: {state.user_query}\nAgent:"
        response = self.llm.chat([{"role": "user", "content": prompt}])
        state.agent_response = response
        state.agent_name = "FlightStatusAgent"
        return state
