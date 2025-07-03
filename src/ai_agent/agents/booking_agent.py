from ..tools.flight_api import search_flights
from ..state.conversation_state import ConversationState
from langchain_core.tools import tool

class BookingAgent:
    def __init__(self, llm=None):
        self.llm = llm  # Optional LLM for prompt handling

    def run(self, state: ConversationState) -> ConversationState:
        """
        Handles booking-related queries using mock tool.
        """
        query = state.user_query.lower()

        if "book" in query or "flight" in query:
            result = search_flights(state)
            state.agent_response = result
        else:
            state.agent_response = "I'm not sure how to help with that booking request."
        
        return state
