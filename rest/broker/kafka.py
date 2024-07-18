import json
from aiokafka import AIOKafkaProducer

kafka_producer = AIOKafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


async def init_kafka_producer():
    await kafka_producer.start()


async def close_kafka_producer():
    await kafka_producer.stop()


async def send_kafka_message(topic: str, message: dict):
    await kafka_producer.send_and_wait(topic, message)
