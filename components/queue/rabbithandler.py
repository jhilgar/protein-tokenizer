import os
import pika

class RabbitHandler():
    def __init__(self):
        if not "CLOUDAMQP" in os.environ:
            url = 'localhost'
        else:
            url = os.getenv("CLOUDAMQP_URL")

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(url))

    def channel(self):
        return self.connection.channel()

    def close(self):
        self.connection.close()