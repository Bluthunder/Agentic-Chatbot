from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.ai_agent.agents.router_agent import RouterAgent
from src.ai_agent.state.conversation_state import ConversationState
import uuid

app = FastAPI()
router_agent = RouterAgent()

# Temporary in-memory session store (use Redis in prod)
session_store = {}

@app.get("/")
def root():
    return {"status": "Agentic Chatbot running"}

@app.websocket("/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    session_store[session_id] = []

    try:
        while True:
            user_input = await websocket.receive_text()

            state = ConversationState(
                session_id=session_id,
                user_query=user_input
            )

            # Run router agent
            updated_state = router_agent.run(state)

            # Store history
            session_store[session_id].append({
                "user": user_input,
                "agent": updated_state.agent_response,
                "intent": updated_state.intent,
                "topic": updated_state.topic,
                "agent_name": updated_state.agent_name
            })

            # Respond
            await websocket.send_json({
                "response": updated_state.agent_response,
                "intent": updated_state.intent,
                "topic": updated_state.topic,
                "sentiment": updated_state.sentiment,
                "routed_to": updated_state.agent_name
            })

    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
        session_store.pop(session_id, None)
