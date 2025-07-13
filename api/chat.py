from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.ai_agent.agents.router_agent import RouterAgent
from src.ai_agent.state.conversation_state import ConversationState
import uuid
import json

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
            try:
                # Receive and parse user input
                raw = await websocket.receive_text()
                data = json.loads(raw)
                user_input = data.get("query")

                if not user_input:
                    await websocket.send_json({"error": "Missing 'query' field in message."})
                    continue
                
                # user_input = await websocket.receive_text()

                state = ConversationState(
                    session_id=session_id,
                    user_query=user_input
                )

                # Run router agent
                updated_state = await router_agent.run(state)

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

            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON format"})
            except Exception as e:
                await websocket.send_json({"error": "Internal server error"})
                print(f"Internal Error: {e}")
                break

    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
        session_store.pop(session_id, None)

    except Exception as e:
        print(f"Internal Error : {e}")
