import io
import re
import json
import datetime
import requests
from requests.adapters import HTTPAdapter, Retry

from Bio import SeqIO

from components.models import SearchRequest, QueryResults
from components.database import DatabaseHandler
from components.api_queue import setup_app

class DataCollector():
    re_next_link = re.compile(r'<(.+)>; rel="next"')

    def __init__(self):
        self.handler = DatabaseHandler()
        self.handler.drop_all()
        self.handler.create_all()

        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter())

    def get_next_link(headers):
        if "Link" in headers:
            match = DataCollector.re_next_link.match(headers["Link"])
            if match:
                return match.group(1)
        
    def get_batch(self, batch_url):
        while batch_url:
            response = self.session.get(batch_url)
            response.raise_for_status()
            total = response.headers["x-total-results"]
            yield response, total
            batch_url = DataCollector.get_next_link(response.headers)

    def get_records(self, batch_url):
        query_id = self.handler.insert_query(batch_url)
        for batch, total in self.get_batch(batch_url):
            for record in SeqIO.parse(io.StringIO(batch.text), "fasta"):
                self.handler.insert_dataset(query_id, str(record.seq))
        return (query_id, total)

app, router = setup_app()
datacollector = DataCollector()

@router.subscriber("datacollector_url")
@router.publisher("backend_query_results")
async def datacollector_url(message: SearchRequest) -> QueryResults:
    query_id, num_results = datacollector.get_records(message.url)
    query_results = QueryResults(
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        source = "datacollector",
        query_id = query_id,
        num_results = num_results
    )
    return query_results
