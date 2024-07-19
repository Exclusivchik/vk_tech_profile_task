from aiokafka.errors import KafkaConnectionError
from fastapi import FastAPI

from rest.broker.kafka import kafka_producer, check_kafka
from rest.controllers.application_controller import router as application_router
from rest.controllers.car_controller import router as car_router

app = FastAPI(
    title="JSON Processor",
)


@app.on_event("startup")
async def startup_event():
    if check_kafka():
        await kafka_producer.start()
    else:
        print("Kafka is not available ")


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()


app.include_router(application_router)
app.include_router(car_router)
