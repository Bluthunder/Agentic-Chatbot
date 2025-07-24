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
        # Separate system and user/assistant messages
        system_prompt = ""
        chat_turns = []

        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            elif msg["role"] == "user":
                chat_turns.append(f"[INST] {msg['content']} [/INST]")
            elif msg["role"] == "assistant":
                chat_turns.append(msg["content"])  # assistant reply continuation

        # Combine prompt
        full_prompt = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n"
        full_prompt += "\n".join(chat_turns)
        print("==== MistralLLM.chat full prompt ====")
        print(full_prompt)
        print("=====================================")


        output = self.llm(full_prompt.strip(), max_tokens=self.max_tokens, temperature=self.temperature)

        print("==== MistralLLM.chat raw output ====")
        print(output)
        print("===================================")
        print(output["choices"][0]["text"].strip())
        print("===================================")
        return output["choices"][0]["text"].strip()


    def name(self) -> str:
        return "mistral-7b-instruct"
