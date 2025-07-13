import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ai_agent.agents.router_agent import RouterAgent
from ai_agent.state.conversation_state import ConversationState

def test_router(query: str):
    router = RouterAgent()
    state = ConversationState(user_query=query)
    updated_state = router.run(state)

    print(f"🔍 Input Query: {query}")
    print(f"🧠 Predicted Intent: {updated_state.intent}")
    print(f"🧭 Routed to Agent: {updated_state.agent_name}")
    print(f"💬 Agent Response: {updated_state.agent_response}")

if __name__ == "__main__":
    queries = [
        "I need help with date change for a booking",
        "When does flight AI202 depart?",
        "Where is my flight right now?",
        "I want to cancel my reservation",
        "Can I change my meal preference?"
    ]

    for query in queries:
        print("\n" + "=" * 80)
        test_router(query)
