import asyncio
import websockets
import json

async def chat():
    uri = "ws://localhost:8000/chat"
    async with websockets.connect(uri) as websocket:
        print("Connected to chatbot. Type your message.")
        while True:
            message = input("You: ")
            await websocket.send(json.dumps({"query": message}))
            response = await websocket.recv()
            data = json.loads(response)
            print(f"Agent [{data['routed_to']}]:", data['response'])

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nSession ended.")   