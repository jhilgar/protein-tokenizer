import requests
from uvicorn import Config

from faststream.rabbit import TestRabbitBroker

from components.models import SearchRequest, QueryResults

def test_search():
    url = 'http://localhost:8000/search'
    stream_url = 'http://localhost:8000/stream'
    query = f'spaghetti'

    search_request = SearchRequest(
        source = "test_search",
        destination = "backend",
        query = query
    )
    
    results_returned = False
    for count, response in enumerate(requests.get(stream_url, stream = True).iter_lines()):
        print(response.decode('utf8'))
        if count == 0:
            requests.post(url, json = search_request.model_dump())
        if count > 20:
            break
        if "num_results" in response.decode('utf8'):
            results_returned = True
            break

    assert results_returned