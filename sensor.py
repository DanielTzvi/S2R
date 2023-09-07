import asyncio
import websockets
import random
import json
import rstr

# Global variable to control server termination
server_running = True


async def send_random_messages(websocket):
    min_lat, max_lat = 30, 32
    min_long, max_long = 34, 36
    aircraft = [rstr.xeger(r'^[0-9a-z]{2}-[0-9a-z]{2,5}$') for x in range(3)]
    counter = 0 

    while True:
        counter += 1
        my_object = {
            'lat': random.uniform(min_lat, max_lat),
            'long': random.uniform(min_long, max_long),
            'altitude': random.uniform(0, 13.0),
            'id': random.choice(aircraft),
            'speed': random.uniform(0, 4024.0),
            'dst': 'BCN',
            'src': 'TLV',
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
            break  # Exit this coroutine and let the outer loop handle reconnection
        except websockets.exceptions.InvalidHandshake:
            await asyncio.sleep(1)
            print("InvalidHandshakeError. Reconnecting...")
            break  # Exit this coroutine and let the outer loop handle reconnection
        except Exception as err:
            await asyncio.sleep(1)
            print(err)
            break

async def main():
    global server_running
    while server_running:
        try:
            async with websockets.serve(send_random_messages, "localhost", 8765):
                await asyncio.Future()  # Keep the event loop running

        except Exception as ex:
            print(f"Error starting WebSocket server: {ex}")
            await asyncio.sleep(1)

def stop_server():
    global server_running
    server_running = False

# Your send_random_messages function here

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        stop_server()
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks()))
    finally:
        loop.close()

