
from src.ai_agent.agents.booking_agent import BookingAgent
from src.ai_agent.state.conversation_state import ConversationState
# from langgraph.graph import StateNode

booking_agent = BookingAgent()

async def booking_node(state: ConversationState) -> ConversationState:
    print(f"state from booking node {state}")
    return await booking_agent.run(state)
