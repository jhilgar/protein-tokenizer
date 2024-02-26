import io
import re
import requests
from requests.adapters import HTTPAdapter, Retry

from Bio import SeqIO

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