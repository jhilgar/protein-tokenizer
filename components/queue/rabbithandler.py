import os
import pika

class RabbitHandler():
    def __init__(self):
        if not "CLOUDAMQP_URL" in os.environ:
            url = 'amqp://localhost:guest@guest/'
        else:
            url = 'amqp://qwfsjbke:gCsf0__NzULPgGx-ES_-z5p8oEDscsD8@woodpecker.rmq.cloudamqp.com/qwfsjbke'

        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)

    def channel(self):
        return self.connection.channel()

    def close(self):
        self.connection.close()