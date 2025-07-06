from ai_agent.agents.flight_status_agent import FlightStatusAgent
from ai_agent.agents.booking_agent import BookingAgent
from ai_agent.state.conversation_state import ConversationState
from ai_agent.tools.llm_loader import get_llm

class RouterAgent:
    def __init__(self):
        self.llm = get_llm()
        self.agents = {
            "flight_status": FlightStatusAgent(),
            "booking": BookingAgent()
        }
        self.valid_intents = set(self.agents.keys())

# review few shot prompt with detailed examples. 
    def detect_intent(self, query: str) -> str:
        system_prompt = ("""
            You are a highly specialized intent classification engine for a travel and event booking platform. Your primary function is to analyze user input and categorize it into one of the predefined intents.

            **Your Task:**
                Read the user's query and classify its primary intent. The user might be asking to book flights, cancel flight, refund and flight status
                **Available Intents:**
                    1.  booking: The user expresses a clear desire to start a new booking process. This includes requests to find, book, reserve, purchase, or get something.
                    2.  out_of_scope: The user's query is not related to initiating a booking. This includes general chit-chat, questions about the weather, requests to cancel or modify an existing booking, or checking a booking status.
            
            **Instructions:**
                - Focus strictly on the user's primary goal.
                - A request to "cancel my flight" is NOT a `booking` intent.
                - A question like "what is the status of my booking?" is NOT a `booking` intent.
                - A general statement like "I want to go to Paris" should be interpreted as an intent to start a `booking`.
                - Your response MUST be a JSON object with a single key, "intent".

                **Examples:**

                User: "Book me a flight to New York for tomorrow."
                {"intent": "booking"}

                User: "I need a hotel room in London from the 5th to the 10th."
                {"intent": "booking"}

                User: "Can you find me a rental car at LAX airport?"
                {"intent": "booking"}

                User: "I need to cancel my reservation."
                {"intent": "out_of_scope"}

                User: "Tell me a joke."
                {"intent": "out_of_scope"}

                User: "Hi there"
                {"intent": "out_of_scope"}           
                            
""")
        try:
            response = self.llm.chat([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ])
            print(f"[RouterAgent] Raw response: {response}")
            intent = response.strip().lower()
            if intent not in self.agents:
                intent = "unknown"
            return intent
        except Exception as e:
            print(f"[RouterAgent] Error during intent detection: {e}")
            return "unknown"


    def run(self, state: ConversationState) -> ConversationState:
        """
        Route to appropriate sub-agent based on user intent.
        """
        state.agent_name = "RouterAgent"
        intent = self.detect_intent(state.user_query)
        state.intent = intent

        agent = self.agents.get(intent)

        if not agent:
            state.agent_response = (
                "Sorry, I couldn't understand your request. "
                "Please ask about flight status or booking."
            )
            return state

        return agent.run(state)
