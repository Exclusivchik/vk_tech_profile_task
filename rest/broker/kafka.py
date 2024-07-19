import json

from aiokafka import AIOKafkaProducer
import socket

kafka_producer = AIOKafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def check_kafka() -> bool:
    port = 9092
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


async def send_kafka_message(topic: str, message: dict):
    if check_kafka():
        await kafka_producer.send(topic, message)
    else:
        print("Kafka is not available ")
