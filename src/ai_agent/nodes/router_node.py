from src.ai_agent.state.conversation_state import ConversationState
from src.ai_agent.agents.router_agent import RouterAgent

router = RouterAgent()

async def route_node(state: ConversationState) -> ConversationState:
    print(">>> [router_node] received state:", state)
    new_state = await router.run(state)
    print(">>> [router_node] returning state:", new_state)
    return new_state


