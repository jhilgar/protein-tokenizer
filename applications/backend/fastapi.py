import asyncio
from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker()
app = FastStream(broker)

async def main():
    await app.run()

@broker.subscriber("routing_key")  # handle messages by routing key
async def handle(msg):
    print(msg)


@app.after_startup
async def test_publish():
    print("test")
    await broker.connect()
    await broker.publish(
        "message",
        "routing_key",  # publish message with routing key
    )

if __name__ == "__main__":
    asyncio.run(main())