
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from src.ai_agent.agents.flight_status_agent import FlightStatusAgent
from src.ai_agent.state.conversation_state import ConversationState


@pytest.fixture
def agent():
    return FlightStatusAgent()

@pytest.mark.parametrize("user_query", [
    "Can you tell me the flight status of AI302?",
    "What's the status of my flight from Mumbai to Delhi?"
])
def test_flight_status_agent(agent, user_query):
    state = ConversationState(user_query=user_query, session_id="test_session_002")
    new_state = agent.run(state)

    assert new_state.agent_response is not None
    assert isinstance(new_state.agent_response, str)
    print("\n✅ Agent response:", new_state.agent_response)
