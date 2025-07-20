# test_graph_run.py (for local testing)

from ai_agent.graph.agent_graph import build_agent_graph
from ai_agent.state.conversation_state import ConversationState

graph = build_agent_graph()

initial_state = ConversationState(session_id="demo", user_query="I need help with booking a flight")

# Run graph step-by-step
result = graph.invoke(initial_state)
print(result.agent_response)
