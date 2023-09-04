import asyncio
import websockets
import random
import time

async def send_random_messages(websocket, path):
    while True:
        message = f"Random message: {random.randint(1, 100)}"
        await websocket.send(message)
        await asyncio.sleep(1)  # Send a message every 1 second

start_server = websockets.serve(send_random_messages, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
