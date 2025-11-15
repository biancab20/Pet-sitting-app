"""create pets table

Revision ID: c58daed31e12
Revises: 
Create Date: 2025-11-15 15:29:26.121745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c58daed31e12'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'pets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('breed', sa.String(length=100), nullable=False),
        sa.Column('size', sa.Enum('small', 'medium', 'large', name='petsize'), nullable=False),
        sa.Column('birthdate', sa.Date, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('pets')
    # drop enum type (important for PostgreSQL, harmless in SQLite)
    op.execute("DROP TYPE IF EXISTS petsize")