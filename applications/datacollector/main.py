import requests

from fastapi import Response
import prometheus_client as pc

from components.models import SearchRequest, QueryResults
from components.database import DatabaseHandler
from components.datacollector import get_single_batch
from components.api_queue import setup_app

app, router = setup_app()
handler = DatabaseHandler()

handler.drop_all()
handler.create_all()

num_queries_submitted = pc.Counter("num_queries_submitted", "The number of queries submitted to UniProt.")
num_query_results = pc.Counter("num_query_results", "The total number of result sequences fetched from UniProt.")

@router.subscriber("datacollector_url")
@router.publisher("backend_query_results")
async def datacollector_url(message: SearchRequest) -> QueryResults:
    query_id = handler.insert_query(message.query)
    
    with requests.Session() as session:
        for record in get_single_batch(session, message.query):
            num_queries_submitted.inc()
            handler.insert_dataset(query_id, record)

    num_results = handler.get_num_query_results(query_id)
    num_query_results.inc(num_results)
    
    query_results = QueryResults(
        destination = "backend",
        source = "datacollector",
        query_id = query_id,
        num_results = num_results
    )
    return query_results

@app.get("/metrics")
async def metrics():
    return Response(content = pc.generate_latest(), media_type = "text/plain")