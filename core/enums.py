from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class TaskStatus(str, Enum):
    assigned = "assigned"
    submitted = "submitted"
