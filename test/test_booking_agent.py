# test/test_booking_agent.py

import pytest
from src.ai_agent.agents.booking_agent import BookingAgent
from src.ai_agent.state.conversation_state import ConversationState

@pytest.fixture
def agent():
    return BookingAgent()

@pytest.mark.parametrize("user_query", [
    "I want to book a flight from Delhi to Mumbai.",
    "Book a ticket from Bangalore to Kolkata for tomorrow."
])

@pytest.mark.skip("NOT YET IMPLEMENTED")
def test_booking_agent(agent, user_query):
    state = ConversationState(user_query)
    new_state = agent.run(state)

    assert new_state.agent_response is not None
    assert isinstance(new_state.agent_response, str)
    print("\n✅ Agent response:", new_state.agent_response)
