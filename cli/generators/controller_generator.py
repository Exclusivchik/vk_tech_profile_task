import os


def get_content(model_name: str):
    lines = []
    lines.append(f'''
from typing import Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy import update, select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from rest.broker.kafka import send_kafka_message
from rest.database_connector import get_async_session
from rest.models.database import json_table
from rest.schemas.generated.{model_name.lower()} import {model_name.capitalize()}
from rest.schemas.state import State
    ''')
    lines.append('# don\'t forget to add this router to your app!!')
    lines.append(f'router = APIRouter(prefix="/{model_name.lower()}", tags=["{model_name.capitalize()}"])')
    lines.append(f'''

@router.post('/')
async def create_document(document: {model_name.capitalize()}, session: AsyncSession = Depends(get_async_session)):
    document_dict = document.dict()
    new_d = {{**document_dict, "state": State.NEW, "json": document_dict}}
    del new_d["configuration"]
    stmt = insert(json_table).values(**new_d)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("document_creation", document.dict())
    return {{"ok": True}}
    ''')

    lines.append(f'''
@router.put('/{{json_id}}/specification')
async def change_specification(json_id: UUID, change_dict: Dict[Any, Any], session: AsyncSession = Depends(get_async_session)):
    query = select(json_table.c.json).where(json_table.c.UUID == json_id)
    json_data = await session.execute(query)
    received_json = json_data.one()[0]
    changed_spec = received_json["configuration"]["specification"] | change_dict
    received_json["configuration"]["specification"] = changed_spec
    try:
        {model_name.capitalize()}.model_validate(received_json)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Types mismatch")
    stmt = update(json_table).where(json_table.c.UUID == json_id).values(json=received_json)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("specification_changing", {{"UUID": json_id.hex, "new_values": change_dict}})
    return received_json | {{"ok": True}}
    ''')

    lines.append(f'''
@router.put('/{{json_id}}/settings')
async def change_settings(json_id: UUID, change_dict: Dict[Any, Any], session: AsyncSession = Depends(get_async_session)):
    query = select(json_table.c.json).where(json_table.c.UUID == json_id)
    json_data = await session.execute(query)
    received_json = json_data.one()[0]
    changed_settings = received_json["configuration"]["settings"] | change_dict
    received_json["configuration"]["settings"] = changed_settings
    try:
        {model_name.capitalize()}.model_validate(received_json)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Types mismatch")
    stmt = update(json_table).where(json_table.c.UUID == json_id).values(json=received_json)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("settings_changing", {{"UUID": json_id.hex, "new_values": change_dict}})
    return received_json | {{"ok": True}}
    ''')

    lines.append(f'''
@router.put('/{{json_id}}/state')
async def change_state(json_id: UUID, state: State, session: AsyncSession = Depends(get_async_session)):
    stmt = update(json_table).where(json_table.c.UUID == json_id).values(state=state)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("state_changing", {{"UUID": json_id.hex, "new_value": state}})
    return {{"state": state}}
    ''')

    lines.append(f'''
@router.delete("/{{json_id}}")
async def delete_document(json_id: UUID, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(json_table).where(json_table.c.UUID == json_id)
    await session.execute(stmt)
    await session.commit()
    await send_kafka_message("document_deletion", {{"UUID": json_id.hex}})
    return {{"ok": True}}
    ''')

    lines.append(f'''
@router.get("/{{json_id}}")
async def get_document(json_id: UUID, session: AsyncSession = Depends(get_async_session)) -> {model_name.capitalize()}:
    query = select(json_table.c.json).where(json_table.c.UUID == json_id)
    json_data = await session.execute(query)
    received_json = json_data.one()[0]
    return Application(**received_json)
    ''')

    lines.append(f'''
@router.get("/{{json_id}}/state")
async def get_state(json_id: UUID, session: AsyncSession = Depends(get_async_session)) -> str:
    query = select(json_table.c.state).where(json_table.c.UUID == json_id)
    state_data = await session.execute(query)
    received_state = state_data.one()[0]
    return received_state
    ''')
    return "\n".join(lines)


def create_controller(path: str, model_name: str):
    content = get_content(model_name)
    with open(path, "w+") as file:
        file.write(content)
    print(f"{model_name.capitalize()} controller has been generated")


def generate_rest_controllers(models_dir: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.py')]

    for model_file in model_files:
        model_name = model_file.split('.')[0].lower()
        controller_path = os.path.join(output_dir, f"{model_name}_controller.py")
        create_controller(controller_path, model_name)

    print(f"Controllers have been generated in {output_dir}")
