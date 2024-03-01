import asyncio
import urllib
import datetime

from sse_starlette.sse import EventSourceResponse
from fastapi import Request

from components.api_queue import setup_app
from components.models import QueryResults, SearchRequest, TrainCommand, TokenizerResults

messages = []

app, router = setup_app()

@router.subscriber("backend_tokenizer_results")
async def backend_tokenizer_results(message: TokenizerResults):
    messages.append(message)

@router.subscriber("backend_query_results")
async def backend_query_results(message: QueryResults):
    messages.append(message)

@app.post("/search")
async def search(message: SearchRequest):
    messages.append(message)
    query = urllib.parse.quote(message.query)
    url = f'https://rest.uniprot.org/uniprotkb/search?format=fasta&query={query}&size=200'
    message.query = url
    await router.broker.publish(message, "datacollector_url")

    messages.append(message)
    return message

@app.post("/train")
async def train(message: TrainCommand):
    messages.append(message)
    await router.broker.publish(message, "dataanalyzer_train")
    return message

@app.get("/stream")
async def stream(message: Request):
    async def event_generator():
        while True:
            if await message.is_disconnected():
                break
            if messages:
                yield messages.pop(0).model_dump_json()
            
            await asyncio.sleep(0.01)
    return EventSourceResponse(event_generator(), ping = 5)