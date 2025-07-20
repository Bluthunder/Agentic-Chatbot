# src/ai_agent/graph/agent_graph.py

from langgraph.graph import StateGraph, END
# from ai_agent.agents.router_agent import RouterAgent
from ai_agent.agents.booking_agent import BookingAgent
from ai_agent.agents.flight_status_agent import FlightStatusAgent
# from ai_agent.agents.post_booking_agent import BaggageAgent
# from ai_agent.agents.base_agent import BaseAgent
from ai_agent.nodes import booking_node, fallback_node, flight_status_node, router_node
from ai_agent.state.conversation_state import ConversationState

# Agent Instances

# router = RouterAgent()
# booking = BookingAgent()
# flight_status = FlightStatusAgent()
# # post_booking = BaggageAgent()  # You may later rename to PostBookingAgent
# # complaint = BaseAgent(name="ComplaintAgent")  # Generic fallback if not defined yet

AGENT_REGISTRY = {
    "booking": booking_node,
    "flight_status": flight_status_node
}
FALLBACK_NODE = fallback_node


# Routing function for langgraph (Router → next agent) 
def route_fn(state: ConversationState) -> str:
    intent = getattr(state, "intent", "").lower()

    if intent in AGENT_REGISTRY:
        return intent
    return "fallback"

# LangGraph builder
def build_agent_graph():
    graph = StateGraph(ConversationState)

    # Define all nodes
    graph.add_node("router", router_node)

    for intent, node_fn in AGENT_REGISTRY.items():
        graph.add_node(intent, node_fn)


    graph.add_node("fallback", FALLBACK_NODE)

    # Set entry point
    graph.set_entry_point("router")

    # Route based on intent
    graph.add_conditional_edges(
        "router", 
        route_fn, 
        {intent : intent for intent in AGENT_REGISTRY} |{"fallback" : "fallback"})

    for intent in AGENT_REGISTRY:
        graph.add_edge(intent, "router")
    graph.add_edge("fallback", "router")

    return graph.compile(async_execution=True)
