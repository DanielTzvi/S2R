import asyncio
import websockets
import random
import json


async def send_random_messages(websocket):
    min_x, max_x = -10, 10
    min_y, max_y = -10, 10
    
    while True:
        my_object = {
            'x': random.uniform(min_x, max_x),
            'y': random.uniform(min_y, max_y),
            'dest': (30, 40),
            'origin': (0, 0)
        }
        json_data = json.dumps(my_object)
        # x = random.uniform(min_x, max_x)
        # y = random.uniform(min_y, max_y)
        # random_point = (x, y)
        await websocket.send(json_data)
        await asyncio.sleep(5)  # Send a message every 1 second

start_server = websockets.serve(send_random_messages, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
