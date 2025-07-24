import redis
import json
from ai_agent.state.conversation_state import ConversationState

# Redis connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

STATE_KEY_PREFIX = "session_state:"

# Save full conversation state
def save_state(session_id: str, state: ConversationState):
    key = f"{STATE_KEY_PREFIX}{session_id}"
    redis_client.set(key, state.model_dump_json())
    redis_client.expire(key, 60 * 60 * 12)  # 12 hours

# Load state if it exists
def load_state(session_id: str) -> ConversationState:
    key = f"{STATE_KEY_PREFIX}{session_id}"
    data = redis_client.get(key)
    if data:
        return ConversationState.model_validate_json(data)
    return None

# Save log entry to Redis list
def log_message(session_id: str, message: dict):
    redis_key = f"session:{session_id}:history"
    redis_client.rpush(redis_key, message)
    redis_client.expire(redis_key, 60 * 60 * 12)

# Retrieve full chat history
def get_history(session_id: str):
    redis_key = f"session:{session_id}:history"
    if not redis_client.exists(redis_key):
        return None
    messages = redis_client.lrange(redis_key, 0, -1)
    return [json.loads(m) for m in messages]

# Expire session
def expire_session(session_id: str, ttl_hours: int = 24):
    redis_client.expire(f"session:{session_id}:history", ttl_hours * 60 * 60)
    redis_client.expire(f"{STATE_KEY_PREFIX}{session_id}", ttl_hours * 60 * 60)
