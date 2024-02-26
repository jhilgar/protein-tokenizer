import time

from applications.datacollector.datacollector import DataCollector
from components.database.databasehandler import DatabaseHandler

collector = DataCollector()
handler = DatabaseHandler()

url = 'https://rest.uniprot.org/uniprotkb/search?format=fasta&query=%28Insulin+AND+%28reviewed%3Atrue%29+AND+%28organism_id%3A9823%29+AND+%28length%3A%5B350+TO+400%5D%29%29&size=500'

query_id = handler.insert_query(url)

for id, seq in collector.get_records(url):
    handler.insert_dataset(query_id, str(seq))

while(True):
    time.sleep(1)