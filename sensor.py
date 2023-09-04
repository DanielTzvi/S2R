import asyncio
import websockets
import random


async def send_random_messages(websocket, path):
    min_x, max_x = -10, 10
    min_y, max_y = -10, 10
    while True:
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        random_point = (x, y)
        await websocket.send(f"Random Point: {random_point}")
        await asyncio.sleep(1)  # Send a message every 1 second

start_server = websockets.serve(send_random_messages, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
