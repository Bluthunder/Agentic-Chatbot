import json
from ai_agent.tools.llm_loader import get_llm
from ai_agent.state.conversation_state import ConversationState
import asyncio
from ai_agent.agents.booking_agent import BookingAgent
from ai_agent.agents.flight_status_agent import FlightStatusAgent
import pdb


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
        self.agent_registry = {
            "BookingAgent": BookingAgent(),
            "FlightStatusAgent": FlightStatusAgent(),
            # "PostBookingAgent": PostBookingAgent(),  # Future use
        }

        self.intent_to_agent = {
            "booking": "BookingAgent",
            "flight_status": "FlightStatusAgent",
            "cancellation": "PostBookingAgent"
        }


    async def classify(self, query):
        messages = [
            {"role": "system", "content": self.classifier_prompt},
            {"role": "user", "content": query},
        ]
        
        # pdb.set_trace()
        try:
            # raw_response = await asyncio.to_thread(self.llm.chat, messages)
            raw_response = self.llm.chat(messages)
            json_output = json.loads(raw_response.strip())
            return json_output
        except json.JSONDecodeError as e:
            print(f" JSON Decode Error: {e} | Raw Response: {raw_response}") # will change this logger
            return {"intent": "unknown" , "sentiment": "neutral", "topic": "unknown"}
        

    async def respond(self, query, state):
        messages = [
            {"role": "system", "content": self.response_prompt},
            {"role": "user", "content": query},
        ]

        try:
            # response = await asyncio.to_thread(self.llm.chat, messages)
            response = self.llm.chat(messages)

            if not response:
                print("[RouterAgent] LLM responded with None")
                state.agent_response = "I am sorry, I didn't understand."
                return state
                # return "I am sorry, i didn;t understand"
            state.agent_response = response

            return state
        
        except Exception as ex:
            print(f'[RouterAgent] error is {ex}')
            state.agent_response = " I am experiencing issue, try again later"
            return state
        
    
    def route_to(self, intent: str) -> str:
        if intent in self.intent_to_agent:
            return self.intent_to_agent[intent]
        else:
            return "self"
    

    async def run(self, state: ConversationState) -> ConversationState:
        

        classification = await self.classify(state.user_query)
        state.intent = classification.get("intent", "unknown")
        state.topic = classification.get("topic", "unknown")
        state.sentiment = classification.get("sentiment", "neutral")

       
        # pdb.set_trace()
        
        last_agent_name = getattr(state, "agent_name", None)
        last_agent = self.agent_registry.get(last_agent_name)

        if last_agent and hasattr(last_agent, "is_complete") and not last_agent.is_complete(state):
            
            state.agent_name = last_agent_name
            print(f"Continuing with {last_agent_name}")
            
            try:
                # state = await asyncio.to_thread(last_agent.run, state)
                state = await last_agent.run(state)

            except Exception as e:

                print(f"{last_agent_name} crashed: {e}")
                state = ConversationState(user_query=state.user_query)
                state.agent_name = last_agent_name
                state.agent_response = f"Oops! {last_agent_name} failed."
            return state
        

        routed_agent_name = self.route_to(state.intent)
        state.agent_name = routed_agent_name

        if routed_agent_name == "self":
            state.agent_name = "RouterAgent"
            # state.agent_response = await self.respond(state.user_query)
            state = await self.respond(state.user_query, state)
            return state
        

        agent = self.agent_registry.get(routed_agent_name)
        if agent:
            try:
                # state = await asyncio.to_thread(agent.run, state)
                state = await agent.run(state)
            except Exception as e:
                print(f"{routed_agent_name} Error: {e}")
                state = ConversationState(user_query=state.user_query)
                state.agent_name = routed_agent_name
                state.agent_response = f"Oops! Something went wrong in {routed_agent_name}."


        else:
            print(f"[RouterAgent] No agent found for: {routed_agent_name}, responding directly")
            state.agent_name = "RouterAgent"
            state.agent_response = await self.respond(state.user_query)

    
        if not getattr(state, "agent_response", None):
            state.agent_response = "I'm sorry, I couldn't understand that. Could you please rephrase?"

        return state

