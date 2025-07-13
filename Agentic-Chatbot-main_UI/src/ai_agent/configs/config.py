import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))           # .../src/ai_agent/configs
AI_AGENT_DIR = os.path.dirname(CONFIG_DIR)                        # .../src/ai_agent
SRC_DIR = os.path.dirname(AI_AGENT_DIR)                           # .../src

# LLM config
LLM_BACKEND = os.getenv("LLM_BACKEND", "mistral")
raw_model_path = os.getenv("MISTRAL_MODEL_PATH", "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")

# Resolve relative model path (if not absolute)
if os.path.isabs(raw_model_path):
    MISTRAL_MODEL_PATH = raw_model_path
else:
    MISTRAL_MODEL_PATH = os.path.join(AI_AGENT_DIR, raw_model_path)


# Validate model file exists (only if using Mistral)
if LLM_BACKEND == "mistral" and not os.path.exists(MISTRAL_MODEL_PATH):
    raise FileNotFoundError(f"[CONFIG] Mistral model not found at path: {MISTRAL_MODEL_PATH}")
