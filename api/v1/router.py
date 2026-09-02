from fastapi import APIRouter

from api.v1.students import router as students_router
from api.v1.teacher import router as teacher_router
from api.v1.courses import router as courses_router
from api.v1.tasks import router as tasks_router
from api.v1.schedules import router as schedules_router

router = APIRouter()

router.include_router(
    students_router,
    prefix='/students',
    tags=['Students']
)

router.include_router(
    teacher_router,
    prefix='/teachers',
    tags=['Teachers']
)

router.include_router(
    courses_router,
    prefix='/courses',
    tags=['Courses']
)

router.include_router(
    tasks_router,
    prefix='/tasks',
    tags=['Tasks']
)

router.include_router(
    schedules_router,
    prefix='/schedules',
    tags=['Schedules']
)