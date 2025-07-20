from langgraph.graph import StateGraph, END
from ai_agent.state.conversation_state import ConversationState

async def end_node(state: ConversationState) -> ConversationState:
    print("✅ Reached end node with agent_response:", state.agent_response)
    return state

def completion_or_router(agent, name: str):
    return lambda state: "router" if not agent.is_complete(state) else "end"

def build_agent_graph(route_node, booking_node, flight_status_node):
    # register_type(ConversationState)
    graph = StateGraph(ConversationState, debug=True)

    # Register nodes
    graph.add_node("router", route_node)
    graph.add_node("booking", booking_node)
    graph.add_node("flight_status", flight_status_node)
    graph.add_node("end", end_node)

    def route_fn(state: ConversationState) -> str:
        intent = getattr(state, "intent", "").lower()
        if intent == ["booking", "flight_search", "ticket", "flight_booking"]:
            return "booking"
        elif intent == "flight_status":
            return "flight_status"
        else:
            return "end"  # generic/greeting/unknown cases

    # Set entry and routing logic
    graph.set_entry_point("router")
    graph.set_finish_point("end")
    graph.add_conditional_edges(
        "router",
        route_fn,
        {"booking": "booking", 
         "flight_status": "flight_status", 
         "end": "end"}
    )

    graph.add_conditional_edges(
    "flight_status",
    lambda state: "router" if not flight_status_node.is_complete(state) else "end",
    {"router": "router", "end": "end"}
    )

    graph.add_conditional_edges(
        "booking",
        lambda state: "router" if not booking_node.is_complete(state) else "end",
        {"router": "router", "end": "end"}
    )

    # graph.add_edge("booking", "router")
    # graph.add_edge("flight_status", "router")


    return graph.compile()