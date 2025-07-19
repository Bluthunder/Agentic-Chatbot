import random
import string
from ..state.conversation_state import ConversationState

def generate_dummy_pnr():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def search_flights(state: ConversationState) -> str:
    """
    Mocked flight search and booking confirmation using user input.
    """
    origin = getattr(state, "origin", "DEL")
    destination = getattr(state, "destination", "CDG")
    travel_date = getattr(state, "travel_date", "in the next few days")

    airlines = ["IndiGo", "Air India", "Vistara", "Lufthansa", "Qatar Airways", "Etihad", "Emirates"]
    selected_airline = random.choice(airlines)
    dummy_pnr = generate_dummy_pnr()

    return (
        f"✈️ Flight booked from {origin} to {destination} on {travel_date}!\n"
        f"🛫 Airline: {selected_airline}\n"
        f"🎟️ PNR: {dummy_pnr}\n"
        f"Would you like hotel suggestions or help with local attractions?"
    )
