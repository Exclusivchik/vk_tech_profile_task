import uuid

from sqlalchemy import MetaData, Table, Column, String, JSON, UUID

metadata = MetaData()

data = Table(
    "data",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("kind", String, nullable=False),
    Column("name", String, nullable=False),
    Column("version", String, nullable=False),
    Column("description", String),
    Column("state", String, nullable=False),
    Column("json", JSON, nullable=False)
)
