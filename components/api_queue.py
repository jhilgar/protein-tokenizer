import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream.rabbit.fastapi import RabbitRouter

def setup_app():
    load_dotenv()

    router = RabbitRouter(os.getenv("CLOUDAMQP_URL"))

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
    
    return (app, router)