import json
from ..tools.llm_loader import get_llm
from ..state.conversation_state import ConversationState


class RouterAgent:
    def __init__(self):
        self.llm = get_llm()

        ## Need to move this to prompt template 
        
        self.classifier_prompt = """You are a classification agent for a travel assistant system.

Given a user's query, your job is to detect and return ONLY the following three attributes in JSON format:

- intent: One of ["booking", "cancellation", "flight_status", "meal_preference", "greeting", "complaint", "unknown"]
- sentiment: One of ["positive", "neutral", "negative"]
- topic: A short one-word category like "booking", "cancellation", "flight", "meals", "support", or "unknown"

⚠️ VERY IMPORTANT: Your response MUST ONLY contain a single JSON object on one line. DO NOT include explanations, greetings, or anything else.

Example:

{"intent": "booking", "sentiment": "neutral", "topic": "booking"}
"""

        self.response_prompt = """You are a helpful travel assistant. Based on the user's query, provide a helpful response in natural language.
"""

    def classify(self, query):
        messages = [
            {"role": "system", "content": self.classifier_prompt},
            {"role": "user", "content": query},
        ]
        raw_response = self.llm.chat(messages)
        try:
            json_output = json.loads(raw_response.strip())
            return json_output
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e} | Raw Response: {raw_response}") # will change this logger
            return {"intent": "unknown" , "sentiment": "neutral", "topic": "unknown"}

    def respond(self, query):
        messages = [
            {"role": "system", "content": self.response_prompt},
            {"role": "user", "content": query},
        ]
        return self.llm.chat(messages)

    def run(self, state: ConversationState) -> ConversationState:
        
        classification = self.classify(state.user_query)
        state.intent = classification.get("intent", "unknown")
        state.topic = classification.get("topic", "unknown")
        state.sentiment = classification.get("sentiment", "neutral")
        state.agent_name = self.route_to(state.intent)
        state.agent_response = self.respond(state.user_query)

        return state

    def route_to(self, intent: str) -> str:
        intent_to_agent = {
            "booking": "BookingAgent",
            "flight_status": "FlightStatusAgent",
            "cancellation": "CancellationAgent",
            "meal_preference": "MealPreferenceAgent"
        }
        return intent_to_agent.get(intent, "RouterAgent")

