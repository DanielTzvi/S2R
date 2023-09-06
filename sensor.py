import asyncio
import websockets
import random
import json

async def send_random_messages(websocket):
    min_x, max_x = -180, 180
    min_y, max_y = -90, 90
    counter = 0
    while True:
        counter += 1
        my_object = {
            'x': random.uniform(min_x, max_x),
            'y': random.uniform(min_y, max_y),
            'destination': (30, 40),
            'source': (0, 0),
            'counter': counter
        }

        json_data = json.dumps(my_object)
        try:
            await websocket.send(json_data)
            await asyncio.sleep(1)  # Send a message every 1 second
            print(counter)
        except websockets.exceptions.ConnectionClosed:
            await asyncio.sleep(1)
            print("ConnectionClosedError. Reconnecting...")
            return  # Exit this coroutine and let the outer loop handle reconnection
        except websockets.exceptions.InvalidHandshake:
            await asyncio.sleep(1)
            print("InvalidHandshakeError. Reconnecting...")
            return  # Exit this coroutine and let the outer loop handle reconnection
        except Exception as err:
            await asyncio.sleep(1)
            print(err)

async def main():
    while True:
        try:
            async with websockets.serve(send_random_messages, "localhost", 8765):
                await asyncio.Future()  # run forever
        except Exception as ex:
            print(f"Error starting WebSocket server: {ex}")
            await asyncio.sleep(1)

asyncio.run(main())
