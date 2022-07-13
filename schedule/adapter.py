import typing

from courses.models import Course
from schedule.Schedule_models import A_Course, A_CourseOffering, A_CourseSection, A_Schedule
from schedule.utils import create_default_section


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
    sections = a_course_offering.sections.all()
    sections_dict_list = []
    for section in sections:
        section_dict = clean_dict(vars(section))
        timeslot_dict_list = []
        # add many-many timeslots to course offering dictionary
        if hasattr(section, "timeslots"):
            for timeslot in section.timeSlots.all():
                timeslot_dict_list.append(vars(timeslot))
        section_dict["timeslots"] = timeslot_dict_list
        sections_dict_list.append(section_dict)
    course_offering_dict = {"course": course_dict, "sections": sections_dict_list}
    return course_offering_dict


def clean_dict(input_dict):
    useless_attributes = ["id", "_state", "_constructor_args", "creation_counter", "_db", "_hints", "core_filters",
                         "instance", "courseOfferings__id", "reverse", "pk_field_names", "prefetch_cache_name",
                         "query_field_name", "related_val", "source_field", "source_field_name", "symmetrical",
                         "target_field", "target_field_name", "target_field_name", "through", "name", "model"]
    for useless_attribute in useless_attributes:
        try:
            del(input_dict[useless_attribute])
        except KeyError:
            pass
    for key in input_dict.keys():
        if type(key) == dict:
            clean_dict(key)
    return input_dict


def course_to_course_offering(course: Course) -> A_CourseOffering:
    a_course = course_to_alg_course(course)
    course_offering = A_CourseOffering.objects.get_or_create(course=a_course)
    if len(course_offering.sections.all()) == 0:
        course_offering.save()
        a01 = create_default_section()
        a01.save()
        a02 = create_default_section()
        a02.save()
        course_offering.sections.set([a01, a02])
    return course_offering


def add_course_offering_to_schedule(course: Course, a_course_offering: A_CourseOffering):
    schedule = A_Schedule.objects.get(id=0)
    if course.fall_offering:
        schedule.fall.add(a_course_offering)
    if course.spring_offering:
        schedule.spring.add(a_course_offering)
    if course.summer_offering:
        schedule.summer.add(a_course_offering)
