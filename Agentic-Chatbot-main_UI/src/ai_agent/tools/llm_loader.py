from ..configs.config import LLM_BACKEND, MISTRAL_MODEL_PATH
from .mistral_llm import MistralLLM
from .base_llm import BaseLLM

_cached_llm = None

def get_llm() -> BaseLLM:
    global _cached_llm
    if _cached_llm:
        return _cached_llm

    if LLM_BACKEND == "mistral":
        _cached_llm = MistralLLM(MISTRAL_MODEL_PATH)
        return _cached_llm
    else:
        raise ValueError(f"Unsupported LLM backend: {LLM_BACKEND}")
