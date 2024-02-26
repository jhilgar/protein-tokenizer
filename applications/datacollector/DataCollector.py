import re
import requests
from requests.adapters import HTTPAdapter, Retry

from ...components.database import DatabaseHandler

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


'''
collector = DataCollector()
url = 'https://rest.uniprot.org/uniprotkb/search?format=fasta&query=%28Insulin+AND+%28reviewed%3Atrue%29+AND+%28organism_id%3A9823%29%29&size=20'
interactions = {}
for batch, total in collector.get_batch(url):
    print(batch.text)
'''