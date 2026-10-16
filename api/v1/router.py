from fastapi import APIRouter

from api.v1.students import router as students_router
from api.v1.teachers import router as teacher_router
from api.v1.courses import router as courses_router
from api.v1.tasks import router as tasks_router
from api.v1.schedules import router as schedules_router
from api.v1.users import router as users_router
from api.v1.auth import router as auth_router

router = APIRouter()

router.include_router(
    students_router
)

router.include_router(
    teacher_router
)

router.include_router(
    courses_router
)

router.include_router(
    tasks_router
)

router.include_router(
    schedules_router
)

router.include_router(
    users_router
)

router.include_router(
    auth_router
)