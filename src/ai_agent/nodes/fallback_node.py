from src.ai_agent.state.conversation_state import ConversationState

async def fallback_node(state: ConversationState) -> ConversationState:
    state.response = "Sorry, I couldn't understand your request. Could you please rephrase?"
    return state