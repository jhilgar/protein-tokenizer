import io
import re
import time
import requests
from requests.adapters import HTTPAdapter, Retry

from Bio import SeqIO

from components.database.databasehandler import DatabaseHandler

# Code adapted from uniprot.org/help/api_queries
class DataCollector():
    re_next_link = re.compile(r'<(.+)>; rel="next"')

    def __init__(self):
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
        for batch, total in self.get_batch(batch_url):
            for record in SeqIO.parse(io.StringIO(batch.text), "fasta"):
                yield record.id, record.seq

if (__name__ == "__main__"):
    collector = DataCollector()
    handler = DatabaseHandler()

    handler.drop_all()
    handler.create_all()

    url = 'https://rest.uniprot.org/uniprotkb/search?format=fasta&query=%28Insulin+AND+%28reviewed%3Atrue%29+AND+%28organism_id%3A9823%29+AND+%28length%3A%5B350+TO+400%5D%29%29&size=500'

    query_id = handler.insert_query(url)

    for id, seq in collector.get_records(url):
        handler.insert_dataset(query_id, str(seq))

    while(True):
        time.sleep(0.5)