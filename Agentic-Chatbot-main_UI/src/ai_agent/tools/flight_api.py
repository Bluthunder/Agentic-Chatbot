from ..state.conversation_state import ConversationState

def search_flights(state: ConversationState) -> str:
    """
    Mocked function to simulate a flight search.
    """
    # Extract mock info from query (you can later do NER or parsing)
    return (
        "✅ Found flights:\n"
        "1. Indigo 6E-203 | DEL → BOM | 9:00 AM - 11:10 AM | ₹4,200\n"
        "2. Air India AI-101 | DEL → BOM | 10:30 AM - 12:45 PM | ₹4,800"
    )
