import os
import asyncio
import threading
from contextlib import asynccontextmanager

from pydantic import BaseModel

from sse_starlette.sse import EventSourceResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from components.queue.rabbithandler import RabbitHandler

class SearchRequest(BaseModel):
    url: str

current_message = None
previous_message = None

rabbit = RabbitHandler()
print(rabbit.connection)
tx = rabbit.channel()
print(tx)
tx.queue_declare('bd')

class Listener(threading.Thread):
    def __init__(self):
        super(Listener, self).__init__()
        self._is_interrupted = False
        self.rabbit = RabbitHandler()
        self.rx = rabbit.channel()
        self.rx.queue_declare('db')

    def stop(self):
        self._is_interrupted = True
        self.rabbit.close()

    def run(self):
        global current_message
        for message in self.rx.consume(queue = 'db', auto_ack = True, inactivity_timeout = 0.1):
            if self._is_interrupted:
                break
            if not all(message):
                continue
            method, properties, body = message
            current_message = body.decode('utf-8')

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rabbit
    consumer_thread = Listener()
    consumer_thread.start()
    yield
    consumer_thread.stop()
    consumer_thread.join()
    rabbit.close()

fastapi = FastAPI(lifespan = lifespan)
origins = ["https://protein-tokenizer-frontend-2bb798acd361.herokuapp.com", "http://localhost:5173"]
fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@fastapi.post("/search")
async def search(request: SearchRequest):
    global tx
    global current_message
    current_message = "search request received from frontend"
    print(request.url)
    tx.basic_publish(exchange='', routing_key='bd', body=request.url)
    return request

@fastapi.get("/stream")
async def message_stream(request: Request):
    async def event_generator():
        global current_message
        global previous_message
        while True:
            if await request.is_disconnected():
                break
            if current_message != previous_message:
                previous_message = current_message
                yield current_message
            await asyncio.sleep(0.1)

    return EventSourceResponse(event_generator())

