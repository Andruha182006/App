from repository.base import CRUDBase
from repository.schedules import ScheduleRepository,schedule_rep
from repository.courses import CourseRepository,course_rep
from repository.teachers import TeacherRepository,teacher_rep
from repository.students import StudentRepository,student_rep
from repository.tasks import TaskRepository,task_rep


__all__ = [
    'CRUDBase',
    'ScheduleRepository',
    'CourseRepository',
    'TeacherRepository',
    'StudentRepository',
    'TaskRepository',
    'schedule_rep',
    'course_rep',
    'teacher_rep',
    'student_rep',
    'task_rep'
]