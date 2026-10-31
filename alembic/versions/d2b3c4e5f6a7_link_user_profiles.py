"""link users to student and teacher profiles

Revision ID: d2b3c4e5f6a7
Revises: c1a2b3d4e5f6
Create Date: 2026-10-31 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd2b3c4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'c1a2b3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add account links and a group to student profiles."""
    op.add_column(
        'students',
        sa.Column('group', sa.String(length=50), nullable=True),
    )
    op.add_column(
        'students',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        'fk_students_user_id_users',
        'students',
        'users',
        ['user_id'],
        ['id'],
        ondelete='SET NULL',
    )
    op.create_unique_constraint('uq_students_user_id', 'students', ['user_id'])

    op.add_column(
        'teachers',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        'fk_teachers_user_id_users',
        'teachers',
        'users',
        ['user_id'],
        ['id'],
        ondelete='SET NULL',
    )
    op.create_unique_constraint('uq_teachers_user_id', 'teachers', ['user_id'])


def downgrade() -> None:
    """Remove profile links and the student group."""
    op.drop_constraint('uq_teachers_user_id', 'teachers', type_='unique')
    op.drop_constraint(
        'fk_teachers_user_id_users',
        'teachers',
        type_='foreignkey',
    )
    op.drop_column('teachers', 'user_id')

    op.drop_constraint('uq_students_user_id', 'students', type_='unique')
    op.drop_constraint(
        'fk_students_user_id_users',
        'students',
        type_='foreignkey',
    )
    op.drop_column('students', 'user_id')
    op.drop_column('students', 'group')
