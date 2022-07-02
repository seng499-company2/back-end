import typing

from courses.models import Course


def course_to_dictionary(course: Course) -> None or typing.Dict[str, str or bool]:
    if course is None:
        return None
    course_dict = vars(course)
    # the state of the django.models object should not be returned
    del(course_dict["_state"])
    return course_dict

