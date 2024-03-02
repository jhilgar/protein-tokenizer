import requests

from components.models import SearchRequest, QueryResults
from components.database import DatabaseHandler
from components.datacollector import get_single_batch
from components.api_queue import setup_app

app, router = setup_app()

handler = DatabaseHandler()

handler.drop_all()
handler.create_all()

@router.subscriber("datacollector_url")
@router.publisher("backend_query_results")
async def datacollector_url(message: SearchRequest) -> QueryResults:
    query_id = handler.insert_query(message.query)
    
    with requests.Session() as session:
        for record in get_single_batch(session, message.query):
            handler.insert_dataset(query_id, record)

    num_results = handler.get_num_query_results(query_id)
    
    query_results = QueryResults(
        destination = "backend",
        source = "datacollector",
        query_id = query_id,
        num_results = num_results
    )
    return query_results
