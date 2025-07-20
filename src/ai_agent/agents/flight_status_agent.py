from ai_agent.agents.base_agent import Agent
from ai_agent.utils.extract_util import extract_flight_number
from ..state.conversation_state import ConversationState
from ai_agent.tools.llm_loader import get_llm
import traceback
import random

from ai_agent.utils.logging_util import get_logger
logger = get_logger(__name__)

class FlightStatusAgent(Agent):

    def __init__(self, llm=None):
        super().__init__(name="FlightStatusAgent", llm=get_llm())
        self.intent = "flight_status"
        self.topic = "check_flight_status"
        self.status_options = ["On Time", "Delayed", "Cancelled", "Departed", "Arrived"]

    async def run(self, state: ConversationState) -> ConversationState:
        try:
            query = state.user_query.lower()

            state.agent_name = self.name
            state.intent = self.intent
            state.topic = self.topic

            flight_number = extract_flight_number(query)
            state.flight_number = flight_number or getattr(state, "flight_number", None)

            if not state.flight_number:
                state.agent_response = "Please provide a valid flight number (e.g., EY 236) to check the status."
            else:
                status = random.choice(self.status_options)
                state.agent_response = f"✈️ Flight {state.flight_number} is currently **{status}**."

        except Exception as e:
            print("FlightStatusAgent Exception:")
            traceback.print_exc()
            state.agent_response = "Oops! Something went wrong in FlightStatusAgent."
            print(f"FlightStatusAgent Error: {e}")

        return state

    def is_complete(self, state: ConversationState) -> bool:
        return bool(state.flight_number and state.agent_response)
