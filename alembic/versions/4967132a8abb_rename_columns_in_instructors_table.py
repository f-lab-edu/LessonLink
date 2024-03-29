"""Rename columns in instructors table

Revision ID: 4967132a8abb
Revises: 896fe20b6c8d
Create Date: 2024-03-16 01:36:56.855192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4967132a8abb'
down_revision: Union[str, None] = '896fe20b6c8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('instructors', 'instructor_id', new_column_name='id',
                    type_=sa.String(length=50), nullable=False)
    op.alter_column('instructors', 'instructor_pw',
                    new_column_name='pw', type_=sa.String(length=50))
    op.alter_column('instructors', 'instructor_name',
                    new_column_name='name', type_=sa.String(length=20))
    op.alter_column('instructors', 'instructor_contact',
                    new_column_name='contact', type_=sa.String(length=20))
    op.alter_column('instructors', 'instructor_email',
                    new_column_name='email', type_=sa.String(length=50))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('instructors', 'id', new_column_name='instructor_id',
                    type_=sa.String(length=50), nullable=False)
    op.alter_column('instructors', 'pw',
                    new_column_name='instructor_pw', type_=sa.String(length=50))
    op.alter_column('instructors', 'name',
                    new_column_name='instructor_name', type_=sa.String(length=20))
    op.alter_column('instructors', 'contact',
                    new_column_name='instructor_contact', type_=sa.String(length=20))
    op.alter_column('instructors', 'email',
                    new_column_name='instructor_email', type_=sa.String(length=20))
    # ### end Alembic commands ###
