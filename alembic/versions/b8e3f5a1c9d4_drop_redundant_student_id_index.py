"""drop redundant index on students.id

Revision ID: b8e3f5a1c9d4
Revises: a7c1e9f4b2d3
Create Date: 2026-10-31 00:10:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b8e3f5a1c9d4'
down_revision: Union[str, Sequence[str], None] = 'a7c1e9f4b2d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop the redundant index; the primary key already has one."""
    op.drop_index('ix_students_id', table_name='students')


def downgrade() -> None:
    """Recreate the redundant index for compatibility."""
    op.create_index('ix_students_id', 'students', ['id'], unique=False)
