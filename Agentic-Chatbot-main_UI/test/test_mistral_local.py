import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ai_agent.tools.llm_loader import get_llm

import pytest

from dotenv import load_dotenv

load_dotenv() 

@pytest.mark.skip("For LLM load test only")
def test_mistral_chat():
    llm = get_llm()

    print(f"🔧 Loaded LLM: {llm.name()}")

    response = llm.chat([
        {"role": "system", "content": "You are a helpful airline assistant."},
        {"role": "user", "content": "What’s the baggage limit for international flights?"}
    ])

    print("\n🛫 Response from LLM:\n")
    print(response)

if __name__ == "__main__":
    test_mistral_chat()
