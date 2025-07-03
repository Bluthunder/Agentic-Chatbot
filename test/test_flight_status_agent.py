
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ai_agent.agents.flight_status_agent import FlightStatusAgent
from ai_agent.state.conversation_state import ConversationState

def test_flight_status_agent():
    agent = FlightStatusAgent()
    state = ConversationState("What’s the current status of flight AI202 from Delhi to Mumbai?")
    new_state = agent.run(state)
    print("Agent Response:", new_state.agent_response)

if __name__ == "__main__":
    test_flight_status_agent()
