import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from ai_agent.agents.router_agent import RouterAgent
from ai_agent.state.conversation_state import ConversationState

@pytest.fixture(scope="module")
def router():
    return RouterAgent()

@pytest.mark.parametrize("query,expected_intent,expected_agent", [
    ("I need help with date change for a booking", "booking", "BookingAgent"),
    ("When does flight AI202 depart?", "flight_status", "FlightStatusAgent"),
    ("Where is my flight right now?", "flight_status", "FlightStatusAgent"),
    ("I want to cancel my reservation", "booking", "BookingAgent"),
    ("Can I change my meal preference?", "booking", "BookingAgent"),
])
def test_router_agent_intents(router, query, expected_intent, expected_agent):
    state = ConversationState(user_query=query)
    updated_state = router.run(state)

    assert updated_state.intent == expected_intent, f"Expected intent: {expected_intent}, got: {updated_state.intent}"
    assert updated_state.agent_name == expected_agent, f"Expected agent: {expected_agent}, got: {updated_state.agent_name}"
    assert updated_state.agent_response is not None
    assert isinstance(updated_state.agent_response, str)
