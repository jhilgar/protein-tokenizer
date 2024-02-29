import asyncio
from sse_starlette.sse import EventSourceResponse
from fastapi import Request

from components.api_queue import setup_app
from components.models import Message, QueryResults, SearchRequest

messages = []

app, router = setup_app()

@router.subscriber("backend")
async def backend(message: Message):
    messages.append(message)

@router.subscriber("backend_query_results")
async def backend_query_results(message: QueryResults):
    messages.append(message)

@app.post("/search")
async def search(request: SearchRequest):
    await router.broker.publish(request, "datacollector_url")
    return request

@app.get("/stream")
async def stream(request: Request):
    async def event_generator():
        global current_message
        global previous_message
        while True:
            if await request.is_disconnected():
                break
            if messages:
                yield messages.pop(0)
            
            await asyncio.sleep(0.01)
    return EventSourceResponse(event_generator())