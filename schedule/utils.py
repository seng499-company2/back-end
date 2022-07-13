from schedule.Schedule_models import A_CourseSection, A_Course
from courses.models import Course


def create_default_section():
    default_section = A_CourseSection()
    default_section.professor = ''
    default_section.capacity = 0
    default_section.save()
    return default_section


def get_alg_course(course: Course) -> A_Course:
    try:
        a_course = A_Course.objects.get(code=course.course_code)
    except A_Course.DoesNotExist:
        a_course = A_Course()
    a_course.code = course.course_code
    a_course.title = course.course_title
    a_course.pengRequired = course.pengRequired
    a_course.yearRequired = course.yearRequired
    return a_course