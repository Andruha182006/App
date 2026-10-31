"""add task submission fields

Revision ID: e3c4d5f6a7b8
Revises: d2b3c4e5f6a7
Create Date: 2026-10-31 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3c4d5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'd2b3c4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add submission status, answer and timestamp to tasks."""
    op.add_column(
        'tasks',
        sa.Column(
            'status',
            sa.String(length=20),
            nullable=False,
            server_default='assigned',
        ),
    )
    op.alter_column('tasks', 'status', server_default=None)
    op.add_column(
        'tasks',
        sa.Column('answer', sa.Text(), nullable=True),
    )
    op.add_column(
        'tasks',
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Remove submission fields from tasks."""
    op.drop_column('tasks', 'submitted_at')
    op.drop_column('tasks', 'answer')
    op.drop_column('tasks', 'status')
