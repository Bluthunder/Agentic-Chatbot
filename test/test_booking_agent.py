

agent = BookingAgent()
state = ConversationState("I want to book a flight from Delhi to Mumbai")

new_state = agent.run(state)
print(new_state.agent_response)
