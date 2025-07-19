from typing import Dict, List, Optional
from pydantic import BaseModel


class ConversationState(BaseModel):
    """
    Holds all the context shared between agents/nodes.
    """
   
    user_query: str = "Hi"
    session_id: str = "12234454"
    agent_response: Optional[str] = "Hi, I am Barry. How can i help you"
    agent_name: Optional[str] = "RouterAgent"
    intent: Optional[str] = "Unknown"
    sentiment: Optional[str] = "Neutral"
    topic: Optional[str] = ""
    metadata: dict = {} 


     # Booking-related slots (add these to avoid dynamic field error)
    origin: Optional[str] = None
    destination: Optional[str] = None
    travel_date: Optional[str] = None
    return_date: Optional[str] = None
    pax: Optional[int] = None
    trip_type: Optional[str] = None  # e.g., 'one_way' or 'round_trip'
    flight_options: Optional[List[Dict]] = None
    booking_confirmed: Optional[bool] = False

