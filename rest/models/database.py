import uuid

from sqlalchemy import MetaData, Table, Column, String, JSON, UUID

metadata = MetaData()

json_table = Table(
    "json_table",
    metadata,
    Column("UUID", UUID, primary_key=True, default=uuid.uuid4),
    Column("kind", String),
    Column("name", String, nullable=False),
    Column("version", String, nullable=False),
    Column("description", String),
    Column("state", String, nullable=False),
    Column("json", JSON, nullable=False)
)
