from src.ai_agent.state.conversation_state import ConversationState
from src.ai_agent.agents.flight_status_agent import FlightStatusAgent

flight_status = FlightStatusAgent()

async def flight_status_node(state: ConversationState) -> ConversationState:
    print(f"state from flight Status node {state}")
    return await flight_status.run(state)