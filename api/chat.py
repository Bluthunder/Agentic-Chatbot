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


# pdb.set_trace()
graph = build_agent_graph(
    route_node,
    booking_node,
    flight_status_node
)
app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

session_store = {}

# router_agent = RouterAgent()
# router_agent.graph = graph


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
               
                raw = await websocket.receive_text()
                data = json.loads(raw)
                user_input = data.get("query")

                if not user_input:
                    await websocket.send_json({"error": "Missing 'query' field in message."})
                    continue
            
                # print("DEBUG: ConversationState module path:", ConversationState.__module__)
                # print("DEBUG: ConversationState class location:", ConversationState.__qualname__)
                # print("DEBUG: ConversationState constructor:", ConversationState.__init__)

                # print("DEBUG: Session ID", session_id)
                # print("DEBUG: UserQuery", user_input)


                state = ConversationState(user_query=user_input, session_id=session_id)

                # Run router agent
                # updated_state = await router_agent.run(state)

                # pdb.set_trace()
                print("🚀 Calling graph.ainvoke with state:", state.model_dump())

                raw_state = await graph.ainvoke(state)
                
                if isinstance(raw_state, dict):
                    updated_state = ConversationState(**raw_state)
                else:
                    updated_state = raw_state 


                # if not updated_state:
                #     await websocket.send_json({
                #         "error": "Internal Error: Agent returned no response."
                #     })
                #     continue

                # agent_response = getattr(updated_state, "agent_response", "I couldn't process that.")
                agent_response = updated_state.agent_response


                redis_key = f'session:{session_id}:history'
                message_log = json.dumps({
                    "user": user_input,
                    "agent": updated_state.agent_response,
                    "intent": updated_state.intent,
                    "topic": updated_state.topic,
                    "sentiment": updated_state.sentiment,
                    "agent_name": updated_state.agent_name
                })

                redis_client.rpush(redis_key, message_log)
                redis_client.expire(redis_key, 60 * 60 * 12 )

                # Respond
                await websocket.send_json({
                    "response": agent_response,
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
        redis_client.expire(f"session:{session_id}:history", 60 * 60 * 24)
        # session_store.pop(session_id, None)

    except Exception as e:
        print(f"Unexpected Error in websocket session {session_id} : {e}")


@app.get("/history/{session_id}")
def get_history(session_id: str):
    redis_key = f"session:{session_id}:history"
    try:
        if not redis_client.exists(redis_key):
            return JSONResponse(status_code=404, content={"error": "Session not found"})

        messages = redis_client.lrange(redis_key, 0, -1)
        parsed_messages = [json.loads(m) for m in messages]

        return {"session_id": session_id, "history": parsed_messages}

    except Exception as e:
        print(f"Error fetching history for session {session_id}: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})