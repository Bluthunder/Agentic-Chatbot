import asyncio
import websockets
import json
# from langsmith import traceable
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ai_agent.utils.logging_util import get_logger
logger = get_logger(__name__)

async def chat():
    uri = "ws://localhost:8000/chat"
    async with websockets.connect(uri) as websocket:
        print("Connected to chatbot. Type your message.")

        while True:
            message = input("You: ").strip()

            if not message:
                continue

            await websocket.send(json.dumps({"query": message}))
            try:

                response = await websocket.recv()
                data = json.loads(response)
                if "error" in data:
                    print(f"Error in data {data['error']}")
                    logger.debug(f'Error in data {data}')
                else:

                    print(f"Agent [{data['routed_to']}]:", data['response'])
                    logger.info(f"Agent {data['routed_to']} ---> {data['response']}")

            except websockets.exceptions.ConnectionClosedOK:
                print("WebSocket connection closed by server.")
                logger.info(f'WebSocket connection closed by server')
                break
            except Exception as e:
                print(f"Error receiving response: {e}")
                logger.info(f'Error receiving response: {e}')
                break

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nSession ended.")  
        logger.info(f"Session Ended") 