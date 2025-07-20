```mermaid

flowchart TD
    subgraph "Agent Nodes"
        RN[router_node] -->|classifies| BookingN[booking_node]
        RN --> FlightStatusN[flight_status_node]
        RN --> FallbackN[fallback_node]
    end

    subgraph "Agent Classes"
        R[RouterAgent] -->|run| RN
        B[BookingAgent] -->|run| BookingN
        F[FlightStatusAgent] -->|run| FlightStatusN
    end

    subgraph "Graph Builder"
        G[graph_factory.py]
        G -->|build_agent_graph| Main
    end

    Main[main/chat.py / FastAPI WebSocket]
    Main -->|await graph.ainvoke state| GraphEngine

    GraphEngine[LangGraph Execution Engine] --> RN
    GraphEngine --> BookingN
    GraphEngine --> FlightStatusN
    GraphEngine --> FallbackN