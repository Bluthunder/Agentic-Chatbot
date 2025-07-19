from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ai_agent.nodes.router_node import route_node
from ai_agent.nodes.booking_node import booking_node
from ai_agent.nodes.flight_status_node import flight_status_node
from ai_agent.agents.router_agent import RouterAgent
from ai_agent.state.conversation_state import ConversationState
from fastapi.responses import JSONResponse
from ai_agent.graph.graph_factory import build_agent_graph
import uuid
import json
import redis 

import pdb

from ai_agent.utils.redis_utils import expire_session, get_history, load_state, log_message, save_state


# pdb.set_trace()
graph = build_agent_graph(
    route_node,
    booking_node,
    flight_status_node
)
app = FastAPI()
# redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# session_store = {}

@app.get("/")
def root():
    return {"status": "Agentic Chatbot running"}

@app.websocket("/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    # session_store[session_id] = []

    try:
        while True:
            try:
               
                raw = await websocket.receive_text()
                data = json.loads(raw)
                user_input = data.get("query")

                if not user_input:
                    await websocket.send_json({"error": "Missing 'query' field in message."})
                    continue
            
                state = load_state(session_id) or ConversationState(user_query=user_input, session_id=session_id)
                state.user_query = user_input

                # prev_state = load_state(session_id)
                # state = ConversationState(user_query=user_input, session_id=session_id)

                # if prev_state:
                #     state.intent = prev_state.intent or state.intent
                #     state.topic = prev_state.topic or state.topic
                #     state.origin = prev_state.origin or state.origin
                #     state.destination = prev_state.destination or state.destination
                #     state.travel_date = prev_state.travel_date or state.travel_date

                # pdb.set_trace()
                print("🚀 Calling graph.ainvoke with state:", state.model_dump())

                raw_state = await graph.ainvoke(state)
                
                if isinstance(raw_state, dict):
                    updated_state = ConversationState(**raw_state)
                else:
                    updated_state = raw_state 

                # agent_response = updated_state.agent_response

                # redis_key = f'session:{session_id}:history'

                save_state(session_id, updated_state)
                
                message_log = json.dumps({
                    "user": user_input,
                    "agent": updated_state.agent_response,
                    "intent": updated_state.intent,
                    "topic": updated_state.topic,
                    "sentiment": updated_state.sentiment,
                    "agent_name": updated_state.agent_name
                })

                log_message(session_id,message_log)

                # redis_client.rpush(redis_key, message_log)
                # redis_client.expire(redis_key, 60 * 60 * 12 )

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
        expire_session(session_id)
        # redis_client.expire(f"session:{session_id}:history", 60 * 60 * 24)
        
    except Exception as e:
        print(f"Unexpected Error in websocket session {session_id} : {e}")


# @app.get("/history/{session_id}")
# def get_history(session_id: str):
#     redis_key = f"session:{session_id}:history"
#     try:
#         if not redis_client.exists(redis_key):
#             return JSONResponse(status_code=404, content={"error": "Session not found"})

#         messages = redis_client.lrange(redis_key, 0, -1)
#         parsed_messages = [json.loads(m) for m in messages]

#         return {"session_id": session_id, "history": parsed_messages}

#     except Exception as e:
#         print(f"Error fetching history for session {session_id}: {e}")
#         return JSONResponse(status_code=500, content={"error": "Internal server error"})
    
@app.get("/history/{session_id}")
def fetch_history(session_id: str):
    history = get_history(session_id)
    if history is None:
        return JSONResponse(status_code=404, content={"error": "Session not found"})
    return {"session_id": session_id, "history": history}