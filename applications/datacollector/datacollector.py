import io
import os
import re
import sys
import time
import requests
from requests.adapters import HTTPAdapter, Retry

import pika
from Bio import SeqIO

from components.database.databasehandler import DatabaseHandler
from components.queue.rabbithandler import RabbitHandler

class DataCollector():
    re_next_link = re.compile(r'<(.+)>; rel="next"')

    def __init__(self):
        self.handler = DatabaseHandler()
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter())

        self.handler.drop_all()
        self.handler.create_all()

        self.rabbit = RabbitHandler()
        self.rx = self.rabbit.channel()
        self.rx.queue_declare(queue = 'datacollector')
        self.rx.basic_consume(queue = 'datacollector', auto_ack = True, on_message_callback = self.callback)

        self.tx = self.rabbit.channel()
        self.tx.queue_declare(queue = 'backend')

    def start(self):
        self.rx.start_consuming()

    def stop(self):
        self.rabbit.close()

    def callback(self, ch, method, properties, body):
        self.tx.basic_publish(exchange = '', routing_key='backend', body='DataCollector: received url from backend')
        query_id = self.handler.insert_query(body)

        for id, seq in self.get_records(body):
            self.handler.insert_dataset(query_id, str(seq))
            self.tx.basic_publish(exchange = '', routing_key='backend', body='DataCollector: search query completed')

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

if __name__ == "__main__":
    try:
        datacollector = DataCollector()
        datacollector.start()
        datacollector.stop()
    except KeyboardInterrupt:
        datacollector.stop()
        try:
            sys.exit(0)
        except:
            os._exit(0)