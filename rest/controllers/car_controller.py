
from typing import Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy import update, select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from rest.broker.kafka import send_kafka_message
from rest.database_connector import get_async_session
from rest.models.database import data
from rest.schemas.generated.car import Car
from rest.schemas.working.state import State
    
# don't forget to add this router to your app!!
router = APIRouter(prefix="/car", tags=["Car"])


@router.post('/')
async def create_document(document: Car, session: AsyncSession = Depends(get_async_session)):
    document_dict = document.dict()
    new_d = {**document_dict, "state": State.NEW, "json": document_dict}
    del new_d["configuration"]
    stmt = insert(data).values(**new_d)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("document_creation", document.dict())
    return {"ok": True}
    

@router.put('/{json_id}/specification')
async def change_specification(json_id: UUID, change_dict: Dict[Any, Any], session: AsyncSession = Depends(get_async_session)):
    query = select(data.c.json).where(data.c.id == json_id)
    json_data = await session.execute(query)
    received_json = json_data.one()[0]
    changed_spec = received_json["configuration"]["specification"] | change_dict
    received_json["configuration"]["specification"] = changed_spec
    try:
        Car.model_validate(received_json)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Types mismatch")
    stmt = update(data).where(data.c.id == json_id).values(json=received_json)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("specification_changing", {"id": json_id.hex, "new_values": change_dict})
    return received_json | {"ok": True}
    

@router.put('/{json_id}/settings')
async def change_settings(json_id: UUID, change_dict: Dict[Any, Any], session: AsyncSession = Depends(get_async_session)):
    query = select(data.c.json).where(data.c.id == json_id)
    json_data = await session.execute(query)
    received_json = json_data.one()[0]
    changed_settings = received_json["configuration"]["settings"] | change_dict
    received_json["configuration"]["settings"] = changed_settings
    try:
        Car.model_validate(received_json)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Types mismatch")
    stmt = update(data).where(data.c.id == json_id).values(json=received_json)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("settings_changing", {"id": json_id.hex, "new_values": change_dict})
    return received_json | {"ok": True}
    

@router.put('/{json_id}/state')
async def change_state(json_id: UUID, state: State, session: AsyncSession = Depends(get_async_session)):
    stmt = update(data).where(data.c.id == json_id).values(state=state)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("state_changing", {"id": json_id.hex, "new_value": state})
    return {"state": state}
    

@router.delete("/{json_id}")
async def delete_document(json_id: UUID, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(data).where(data.c.id == json_id)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("document_deletion", {"id": json_id.hex})
    return {"ok": True}
    

@router.get("/{json_id}")
async def get_document(json_id: UUID, session: AsyncSession = Depends(get_async_session)) -> Car:
    query = select(data.c.json).where(data.c.id == json_id)
    json_data = await session.execute(query)
    received_json = json_data.one()[0]
    return Car(**received_json)
    

@router.get("/{json_id}/state")
async def get_state(json_id: UUID, session: AsyncSession = Depends(get_async_session)) -> str:
    query = select(data.c.state).where(data.c.id == json_id)
    state_data = await session.execute(query)
    received_state = state_data.one()[0]
    return received_state
    