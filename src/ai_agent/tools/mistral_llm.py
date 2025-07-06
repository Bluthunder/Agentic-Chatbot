from llama_cpp import Llama
from .base_llm import BaseLLM
import os

class MistralLLM(BaseLLM):
    def __init__(self, model_path: str, max_tokens: int = 512, temperature: float = 0.7):
        self.model_path = model_path
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=os.cpu_count() or 4,
            n_gpu_layers=35,  # GPU acceleration on Mac M1/M2/M4
            use_mlock=True
        )
        self.max_tokens = max_tokens
        self.temperature = temperature

    def chat(self, messages: list[dict]) -> str:
        response = self.llm.create_chat_completion(messages=messages)
        return response['choices'][0]['message']['content']


    def name(self) -> str:
        return "mistral-7b-instruct"
