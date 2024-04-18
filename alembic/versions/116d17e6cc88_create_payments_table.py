"""Create Payments Table

Revision ID: 116d17e6cc88
Revises: ab6c0a58f4fe
Create Date: 2024-04-19 05:48:42.063879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '116d17e6cc88'
down_revision: Union[str, None] = 'ab6c0a58f4fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'payments',
        sa.Column('uid', sa.String(length=50),
                  nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=8), nullable=False),
        sa.Column('is_paid_ok', sa.Boolean(), nullable=False),
        sa.Column('student_id', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], [
                                'students.id'], name='fk_payments_students', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('uid')
    )


def downgrade() -> None:
    op.drop_table('payments')
