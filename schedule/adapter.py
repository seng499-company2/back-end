import typing

from courses.models import Course
from schedule.Schedule_models import A_Course


def course_to_alg_dictionary(course: Course) -> None or typing.Dict[str, str or bool]:
    if course is None:
        return None
    a_course = course_to_alg_course(course)
    course_dict = vars(a_course)
    # the state of the django.models object should not be returned
    del(course_dict["_state"])
    return course_dict


def course_to_alg_course(course: Course) -> None or A_Course:
    try:
        a_course = A_Course.objects.get(code=course.course_code)
    except A_Course.DoesNotExist:
        a_course = A_Course()
    a_course.code = course.course_code
    a_course.title = course.course_title
    a_course.pengRequired = course.pengRequired
    a_course.yearRequired = course.yearRequired
    a_course.save()
    return a_course


def remove_state(input_dict):
    del(input_dict["_state"])
    return input_dict


def remove_id(input_dict):
    del(input_dict["id"])
    return input_dict
