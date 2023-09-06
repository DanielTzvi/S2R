import asyncio
import websockets
import os
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from dotenv import load_dotenv
import json


def error(e):
    print(str(e))


async def receive_messages():
    load_dotenv()

    EVENT_HUB_CONNECTION_STR = os.getenv('EVENT_HUB_CONNECTION_STR')
    EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME')

    uri = "ws://localhost:8765"
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME, on_error=error)
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    response = await websocket.recv()
                    print("type:", type(response))
                    print(f"Received: {response}")
                    # the event hub name.

                    async with producer:
                        # Create a batch.
                        event_data_batch = await producer.create_batch()

                        # Handasah adds calculations here
                        # Response calculations

                        # Add events to the batch.
                        event_data_batch.add(EventData(response))

                        # Send the batch of events to the event hub.
                        await producer.send_batch(event_data_batch)
                        print('sent data to event hub')
        except Exception as e:
            print(str(e))
asyncio.get_event_loop().run_until_complete(receive_messages())
