import os
import json
import asyncio
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream.rabbit.fastapi import RabbitRouter
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

class SearchRequest(BaseModel):
    url: str

class StatusMessage(BaseModel):
    source: str

class DatacollectorStatus(StatusMessage):
    query_id: int
    num_results: int

current_message = None
previous_message = None

if not "CLOUDAMQP_URL" in os.environ:
    url = 'amqp://localhost:guest@guest/'
else:
    url = os.getenv("CLOUDAMQP_URL")

router = RabbitRouter(url)

app = FastAPI(lifespan = router.lifespan_context)
app.include_router(router)

origins = [ 
    "https://protein-tokenizer-frontend-2bb798acd361.herokuapp.com", 
    "http://localhost:5173" ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    )

@router.subscriber("backend")
async def backend(message: StatusMessage):
    global current_message
    current_message = json.loads(message)

@app.post("/search")
async def search(request: SearchRequest):
    print(request)
    await router.broker.publish(request.url, "datacollector")
    return request

@app.get("/stream")
async def stream(request: Request):
    async def event_generator():
        global current_message
        global previous_message
        while True:
            if await request.is_disconnected():
                break
            if previous_message != current_message:
                previous_message = current_message
                yield current_message
            
            await asyncio.sleep(0.05)
    return EventSourceResponse(event_generator())