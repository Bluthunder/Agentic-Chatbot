from ai_agent.agents.base_agent import Agent
from ..tools.flight_api import search_flights
from ..state.conversation_state import ConversationState
from langchain_core.tools import tool
from ai_agent.tools.llm_loader import get_llm
import spacy
from dateutil.parser import parse as date_parse
from src.ai_agent.utils.iata_codes import CITY_TO_IATA
import traceback

nlp = spacy.load("en_core_web_sm")


class BookingAgent(Agent):
    nlp = spacy.load("en_core_web_sm")

    def __init__(self, llm=None):
        # self.llm = llm  # Optional LLM for prompt handling
        super().__init__(name="BookingAgent", llm=get_llm())
        self.intent="flight_booking"
        self.topic="book_flight"

    
    def extract_details(self, query:str):

        query = query.lower()
        doc = self.nlp(query)

        cities = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
        dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

        origin_city = cities[0].lower() if len(cities) > 0 else None
        destination_city = cities[1].lower() if len(cities) > 1 else None

        origin = CITY_TO_IATA.get(origin_city, "DEL") if origin_city else "DEL"
        destination = CITY_TO_IATA.get(destination_city, "JFK") if destination_city else "JFK"

        travel_date = None
        if dates:
            try:
                dt = date_parse(dates[0], fuzzy=True)
                travel_date = dt.strftime("%Y-%m-%d")
            except Exception:
                pass

        print(f"🧠 NER result: cities={cities}, dates={dates}")

        return origin, destination, travel_date
    

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
            
            origin, destination, travel_date =  self.extract_details(query=query)
            state.origin = origin
            state.destination = destination
            state.travel_date = travel_date

            missing = []
            if not origin or origin == "DEL":
                missing.append("departure city")
            if not destination or destination == "JFK":
                missing.append("destination city")
            if not travel_date:
                missing.append("travel date")

            if missing:
                state.agent_response = (
                    f"To help you book a flight, please provide your "
                    + ", ".join(missing)
                    + "."
                )
            elif "book" in query or "flight" in query or "ticket" in query:
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