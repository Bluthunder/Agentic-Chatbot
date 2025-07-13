from typing import Optional

class ConversationState:
    """
    Holds all the context shared between agents/nodes.
    """
    def __init__(self, user_query: str, session_id: str):
        self.user_query: str = user_query
        self.session_id: str = session_id
        self.agent_response: Optional[str] = None
        self.agent_name: Optional[str] = "BookingAgent"  # update as needed
        self.intent: Optional[str] = None  # For routing logic
        self.metadata: dict = {}  # For internal use, like timestamps or user_id
