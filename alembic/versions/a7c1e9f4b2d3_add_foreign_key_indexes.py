"""add indexes for foreign keys

Revision ID: a7c1e9f4b2d3
Revises: 18003a9c1719
Create Date: 2026-10-30 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a7c1e9f4b2d3'
down_revision: Union[str, Sequence[str], None] = '18003a9c1719'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_INDEXES = (
    ('ix_courses_teacher_id', 'courses', 'teacher_id'),
    ('ix_tasks_student_id', 'tasks', 'student_id'),
    ('ix_tasks_teacher_id', 'tasks', 'teacher_id'),
    ('ix_schedules_course_id', 'schedules', 'course_id'),
    ('ix_schedules_teacher_id', 'schedules', 'teacher_id'),
)


def upgrade() -> None:
    """Create indexes for columns used in foreign-key filters."""
    for index_name, table_name, column_name in _INDEXES:
        op.create_index(index_name, table_name, [column_name], unique=False)


def downgrade() -> None:
    """Drop the foreign-key indexes."""
    for index_name, table_name, _ in reversed(_INDEXES):
        op.drop_index(index_name, table_name=table_name)
