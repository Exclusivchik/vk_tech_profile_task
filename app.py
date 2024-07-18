from fastapi import FastAPI

from rest.broker.kafka import kafka_producer
from rest.controllers.application_controller import router as application_router

app = FastAPI(
    title="JSON Processor",
)


@app.on_event("startup")
async def startup_event():
    await kafka_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()


app.include_router(application_router)
