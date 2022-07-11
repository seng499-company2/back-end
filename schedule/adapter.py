import typing

from courses.models import Course
from schedule.Schedule_models import A_Course, A_CourseOffering, A_CourseSection


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


def a_course_offering_to_dict(a_course_offering: A_CourseOffering):
    course: A_Course = a_course_offering.course
    course_dict = clean_dict(vars(course))
    sections: A_CourseSection = a_course_offering.sections
    sections_dict = clean_dict(vars(sections))
    print(sections)
    print(sections_dict)
    course_offering_dict = {"course": course_dict, "sections": sections_dict}
    return course_offering_dict


def clean_dict(input_dict):
    try:
        del(input_dict["id"])
    except KeyError:
        pass
    try:
        del (input_dict["_state"])
    except KeyError:
        pass
    try:
        del (input_dict["_constructor_args"])
    except KeyError:
        pass
    try:
        del (input_dict["creation_counter"])
    except KeyError:
        pass
    try:
        del (input_dict["_db"])
    except KeyError:
        pass
    try:
        del (input_dict["_hints"])
    except KeyError:
        pass
    try:
        del (input_dict["core_filters"])
    except KeyError:
        pass
    try:
        del (input_dict["instance"])
    except KeyError:
        pass
    try:
        del (input_dict["courseOfferings__id"])
    except KeyError:
        pass
    try:
        del (input_dict["reverse"])
    except KeyError:
        pass
    try:
        del (input_dict["pk_field_names"])
    except KeyError:
        pass
    try:
        del (input_dict["prefetch_cache_name"])
    except KeyError:
        pass
    try:
        del (input_dict["query_field_name"])
    except KeyError:
        pass
    try:
        del (input_dict["related_val"])
    except KeyError:
        pass
    try:
        del (input_dict["source_field"])
    except KeyError:
        pass
    try:
        del (input_dict["source_field_name"])
    except KeyError:
        pass
    try:
        del (input_dict["symmetrical"])
    except KeyError:
        pass
    try:
        del (input_dict["target_field"])
    except KeyError:
        pass
    try:
        del (input_dict["target_field_name"])
    except KeyError:
        pass
    try:
        del (input_dict["target_field_name"])
    except KeyError:
        pass
    try:
        del (input_dict["through"])
    except KeyError:
        pass
    try:
        del (input_dict["name"])
    except KeyError:
        pass
    try:
        del (input_dict["model"])
    except KeyError:
        pass
    try:
        del (input_dict["sections"])
    except KeyError:
        pass
    for key in input_dict.keys():
        if type(key) == dict:
            clean_dict(key)
    # keys_to_delete = []
    # for key in input_dict.keys():
    #     if type(key) == dict:
    #         print("KEY.keys: " + str(key.keys()))
    #     if type(key) == dict and key.keys() == []:
    #         keys_to_delete.append(key)
    #
    # for key in keys_to_delete:
    #     del(input_dict[key])

    for key in input_dict.keys():
        if type(key) == dict:
            clean_dict(key)

    return input_dict
