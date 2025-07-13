from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from src.ai_agent.agents.router_agent import RouterAgent
from src.ai_agent.state.conversation_state import ConversationState
import uuid
import json
import os
from src.ai_agent.models.chat_session import ChatSession, SQLiteSession, PostgresSession, create_all_tables, move_session_to_postgres, get_session_by_id

app = APIRouter()
router_agent = RouterAgent()

# Ensure tables exist at startup
create_all_tables()

# Temporary in-memory session store (use Redis in prod)
session_store = {}

@app.get("/")
def root():
    return {"status": "Agentic Chatbot running"}

@app.get("/session/{session_id}")
def get_session(session_id: str):
    print(f"[DEBUG] Retrieving session {session_id}")
    session_obj = get_session_by_id(session_id)
    if session_obj:
        print(f"[DEBUG] Session {session_id} found in {'Postgres' if session_obj.is_long else 'SQLite'}")
        return {"session_id": session_obj.session_id, "messages": json.loads(session_obj.messages), "is_long": session_obj.is_long}
    print(f"[DEBUG] Session {session_id} not found")
    return {"error": "Session not found"}

@app.websocket("/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    # Accept session_id as a query parameter
    session_id = websocket.query_params.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    if session_id not in session_store:
        session_store[session_id] = []

    # Save empty session to DB immediately if not present
    messages_json = json.dumps(session_store[session_id])
    db = SQLiteSession()
    session_obj = db.query(ChatSession).filter_by(session_id=session_id).first()
    if not session_obj:
        print(f"[DEBUG] Creating empty session {session_id} in SQLite on connect")
        session_obj = ChatSession(session_id=session_id, messages=messages_json, is_long=False)
        db.add(session_obj)
        db.commit()
    db.close()

    # Send session_ready message to frontend
    await websocket.send_json({
        "type": "session_ready",
        "session_id": session_id
    })

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

            # --- DB Save Logic ---
            messages_json = json.dumps(session_store[session_id])
            is_long = len(session_store[session_id]) > 20 or len(messages_json) > 10_000

            if not is_long:
                print(f"[DEBUG] Saving session {session_id} to SQLite (short session)")
                db = SQLiteSession()
                session_obj = db.query(ChatSession).filter_by(session_id=session_id).first()
                if not session_obj:
                    session_obj = ChatSession(session_id=session_id, messages=messages_json, is_long=False)
                    db.add(session_obj)
                else:
                    session_obj.messages = messages_json
                db.commit()
                db.close()
            else:
                print(f"[DEBUG] Moving session {session_id} to Postgres (long session)")
                # Move to Postgres if not already there
                move_session_to_postgres(session_id)
                db = PostgresSession()
                session_obj = db.query(ChatSession).filter_by(session_id=session_id).first()
                if not session_obj:
                    session_obj = ChatSession(session_id=session_id, messages=messages_json, is_long=True)
                    db.add(session_obj)
                else:
                    session_obj.messages = messages_json
                db.commit()
                db.close()

            # Respond
            await websocket.send_json({
                "response": updated_state.agent_response,
                "intent": updated_state.intent,
                "topic": updated_state.topic,
                "sentiment": updated_state.sentiment,
                "routed_to": updated_state.agent_name,
                "session_id": session_id
            })

    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
        session_store.pop(session_id, None)
