```mermaid

graph TD
    %% UI Layer
    subgraph UI["🖥️ User Interface Layer"]
        A1["User Interface - React/Streamlit"]
    end
    
    %% API Layer
    subgraph API["🔧 API Layer"]
        A2["FastAPI Backend"]
        A3["RouterAgent - LangGraph Node"]
    end
    
    %% Downstream Agents
    subgraph AGENTS["🤖 Intelligent Agents"]
        A4a["BookingAgent"]
        A4b["PostBookingAgent"]
        A4c["FlightStatusAgent"]
        A4d["ComplaintAgent"]
    end
    
    %% Model Inference
    subgraph MODEL["🧠 AI Model Layer"]
        B1["Mistral LLM - finetuned"]
    end
    
    %% State Layer
    subgraph STATE["💾 Data Storage Layer"]
        C1["Redis - Short-term State"]
        C2["PostgreSQL - Long-term Logs"]
    end
    
    %% Monitoring Layer
    subgraph MONITOR["📊 Observability Layer"]
        D1["Prometheus Exporter"]
        D2["Grafana Dashboards"]
        D3["OpenTelemetry Tracer"]
    end
    
    %% Flow
    A1 -->|POST /chat| A2
    A2 -->|Route to LangGraph| A3
    A3 -->|Intent: booking| A4a
    A3 -->|Intent: cancellation/refund| A4b
    A3 -->|Intent: flight_status| A4c
    A3 -->|Intent: complaint| A4d
    A3 -->|Generic query| B1
    A4a -->|Multi-turn| B1
    A4b -->|Multi-turn| B1
    A4c -->|LLM + Reasoning| B1
    A4d -->|Complaint workflow| B1
    A3 -->|Session state| C1
    A2 -->|Save chat logs| C2
    A2 -->|Metrics| D1
    A2 -->|Trace| D3
    D1 --> D2
    D3 --> D2
    
    %% Enhanced Color Styling
    classDef uiClass fill:#2196f3,stroke:#0d47a1,stroke-width:3px,color:#fff
    classDef apiClass fill:#9c27b0,stroke:#4a148c,stroke-width:3px,color:#fff
    classDef agentClass fill:#ff9800,stroke:#e65100,stroke-width:3px,color:#fff
    classDef modelClass fill:#4caf50,stroke:#1b5e20,stroke-width:3px,color:#fff
    classDef stateClass fill:#f44336,stroke:#b71c1c,stroke-width:3px,color:#fff
    classDef monitorClass fill:#607d8b,stroke:#263238,stroke-width:3px,color:#fff
    
    class A1 uiClass
    class A2,A3 apiClass
    class A4a,A4b,A4c,A4d agentClass
    class B1 modelClass
    class C1,C2 stateClass
    class D1,D2,D3 monitorClass