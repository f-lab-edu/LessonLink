"""Resize pw column in students and instructors table

Revision ID: e195ba6b081c
Revises: 4967132a8abb
Create Date: 2024-03-16 02:18:27.639478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e195ba6b081c'
down_revision: Union[str, None] = '4967132a8abb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('students', 'pw', type_=sa.String(length=255))
    op.alter_column('instructors', 'pw', type_=sa.String(length=255))


def downgrade() -> None:
    op.alter_column('students', 'pw', type_=sa.String(length=50))
    op.alter_column('instructors', 'pw', type_=sa.String(length=50))
