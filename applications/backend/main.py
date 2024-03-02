import asyncio
import urllib
from typing import Callable


from sse_starlette.sse import EventSourceResponse
from fastapi import Request, Response

import prometheus_client as pc

from components.api_queue import setup_app
from components.models import QueryResults, SearchRequest, TrainCommand, TokenizerResults

messages = []
num_messages_sent = pc.Counter("num_rabbit_sent", "The number of RabbitMQ messages sent.")
num_messages_received = pc.Counter("num_rabbit_received", "The number of RabbitMQ messages received.")
num_streaming_clients_active = pc.Gauge("num_streaming_clients_active", "The number of frontend clients connected to the backend.")
app, router = setup_app()

# todo write hooks for rabbit send/receive methods that automatically handle message logging/processing

@router.subscriber("backend_tokenizer_results")
async def backend_tokenizer_results(message: TokenizerResults):
    num_messages_received.inc()
    messages.append(message)

@router.subscriber("backend_query_results")
async def backend_query_results(message: QueryResults):
    num_messages_received.inc()
    messages.append(message)

@app.post("/search")
async def search(message: SearchRequest):
    num_messages_received.inc()
    messages.append(message)
    query = urllib.parse.quote(message.query)
    url = f'https://rest.uniprot.org/uniprotkb/search?format=fasta&query={query}&size=200'
    message.query = url
    await router.broker.publish(message, "datacollector_url")
    num_messages_sent.inc()
    return message

@app.post("/train")
async def train(message: TrainCommand):
    messages.append(message)
    await router.broker.publish(message, "dataanalyzer_train")
    num_messages_sent.inc()
    return message

@app.get("/stream")
async def stream(message: Request):
    async def event_generator():
        num_streaming_clients_active.inc()
        try:
            while True:
                if await message.is_disconnected():
                    num_streaming_clients_active.dec()
                    break
                if messages:
                    yield messages.pop(0).model_dump_json()
                await asyncio.sleep(0.9)
        except asyncio.CancelledError as e:
            num_streaming_clients_active.dec()
            raise e
            
    return EventSourceResponse(event_generator(), ping = 1, send_timeout=10)

@app.get("/metrics")
async def metrics():
    return Response(content = pc.generate_latest(), media_type = "text/plain")