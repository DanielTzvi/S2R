import asyncio
import websockets
import random
import json
import rstr


async def send_random_messages(websocket):
    min_lat, max_lat = 30, 32
    min_long, max_long = 34, 36
    plains = [rstr.xeger(r'^[0-9a-z]{2}-[0-9a-z]{2,5}$') for x in range(3)]

    while True:
        my_object = {
            'lat': random.uniform(min_lat, max_lat),
            'long': random.uniform(min_long, max_long),
            'altitude': random.uniform(0, 13.0),
            'id': random.choice(plains),
            'speed': random.uniform(0, 4024.0),
            'dst': 'BCN',
            'src': 'TLV'
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
