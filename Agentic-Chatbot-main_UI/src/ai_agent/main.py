import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from ai_agent.state.conversation_state import ConversationState
from ai_agent.agents.router_agent import RouterAgent

def main():
    query = input("✈️  Ask your airline support question: ")
    session_id = "cli_session_" + str(hash(query))[:8]  # Generate a simple session ID for CLI
    state = ConversationState(user_query=query, session_id=session_id)
    router = RouterAgent()

    final_state = router.run(state)

    print(f"\n🧠 Agent: {final_state.agent_name}")
    print(f"💬 Response: {final_state.agent_response}")

if __name__ == "__main__":
    main()
