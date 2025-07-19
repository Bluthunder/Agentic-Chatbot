from ai_agent.agents.base_agent import Agent
from ai_agent.utils.extract_util import extract_flight_details
from ..tools.flight_api import search_flights
from ..state.conversation_state import ConversationState
from ai_agent.tools.llm_loader import get_llm
from src.ai_agent.utils.iata_codes import CITY_TO_IATA
import traceback


class BookingAgent(Agent):

    def __init__(self, llm=None):
        # self.llm = llm  # Optional LLM for prompt handling
        super().__init__(name="BookingAgent", llm=get_llm())
        self.intent= "flight_booking"
        self.topic="book_flight"


    async def run(self, state: ConversationState) -> ConversationState:
        """
        Handles booking-related queries using mock flight booking api.
        """
        try:

            query = state.user_query.lower()
            # Set routing info
            state.agent_name = self.name
            state.intent = self.intent
            state.topic = self.topic
            
            origin, destination, travel_date =  extract_flight_details(query)
            state.origin = origin or state.origin
            state.destination = destination or state.destination
            state.travel_date = travel_date or state.travel_date

            missing = []
            if not origin:
                missing.append("departure city")
            if not destination:
                missing.append("destination city")
            if not travel_date:
                missing.append("travel date")

            if missing:
                state.agent_response = (
                    f"To help you book a flight, please provide your "
                    + ", ".join(missing)
                    + "."
                )
            elif any(k in query for k in ["book", "flight", "ticket"]):
                print(f"📤 BookingAgent extracted: origin={origin}, destination={destination}, date={travel_date}")

                result = search_flights(state)
                state.agent_response = result
            else:
                state.agent_response = "I can help you with flight bookings. Where would you like to go?"
        
        except Exception as e:
            print("BookingAgent Exception:")
            traceback.print_exc()
            state.agent_response = "Oops! Something went wrong in BookingAgent."
            print(f"BookingAgent Error: {e}")

        return state
    
    def is_complete(self, state: ConversationState) -> bool:
        return all([
            getattr(state, "origin", None),
            getattr(state, "destination", None),
            getattr(state, "travel_date", None)
        ])