import requests
import time
import contextlib
import threading
import uvicorn
import pytest

from faststream.rabbit import TestRabbitBroker

from applications.backend.main import backend_query_results
from components.models import SearchRequest, QueryResults

class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()

@pytest.mark.asyncio
async def test_search():
    url = 'http://localhost:4321/search'
    query = f'https://rest.uniprot.org/uniprotkb/search?format=fasta&query=spaghetti&size=2'

    search_request = SearchRequest(
        source = "test_search",
        destination = "backend",
        query = query
    )
    backend_config = uvicorn.Config("applications.backend.main:app", host = "0.0.0.0", port = 4321)
    backend_server = Server(config = backend_config)

    datacollector_config = uvicorn.Config("applications.datacollector.main:app", host = "0.0.0.0", port = 8080)
    datacollector_server = Server(config = datacollector_config)

    with backend_server.run_in_thread(), datacollector_server.run_in_thread():
        requests.post(url = url, json = search_request.model_dump())

