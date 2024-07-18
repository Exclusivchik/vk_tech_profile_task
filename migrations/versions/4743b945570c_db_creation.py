"""DB creation

Revision ID: 4743b945570c
Revises: 
Create Date: 2024-07-14 19:26:59.246196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4743b945570c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('json_table',
                    sa.Column('UUID', sa.UUID(), nullable=False),
                    sa.Column('kind', sa.String(), nullable=True),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('version', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('json', sa.JSON(), nullable=False),
                    sa.PrimaryKeyConstraint('UUID')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('json_table')
    # ### end Alembic commands ###