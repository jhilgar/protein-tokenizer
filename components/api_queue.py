import os
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream.rabbit.fastapi import RabbitRouter

def setup_app():
    if not "CLOUDAMQP_URL" in os.environ:
        url = 'amqp://guest:guest@localhost/'
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
    
    return (app, router)