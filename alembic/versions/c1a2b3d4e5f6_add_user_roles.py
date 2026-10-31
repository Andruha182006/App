"""add user roles

Revision ID: c1a2b3d4e5f6
Revises: b8e3f5a1c9d4
Create Date: 2026-10-31 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1a2b3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'b8e3f5a1c9d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add a role to users and promote existing superusers to admin."""
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(length=20),
            nullable=False,
            server_default='student',
        ),
    )
    op.execute("UPDATE users SET role = 'admin' WHERE is_superuser = true")
    op.alter_column('users', 'role', server_default=None)


def downgrade() -> None:
    """Remove the role column."""
    op.drop_column('users', 'role')
