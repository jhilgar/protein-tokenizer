import os
import pika

class RabbitHandler():
    def __init__(self):
        if not "CLOUDAMQP_URL" in os.environ:
            url = 'amqp://localhost:guest@guest/'
        else:
            url = os.getenv("CLOUDAMQP_URL")

        print(f"using {url} to connecto to cloud amqp")
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)

    def channel(self):
        return self.connection.channel()

    def close(self):
        self.connection.close()