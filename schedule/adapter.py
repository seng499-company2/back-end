from courses.models import Course
from schedule.Schedule_models import A_Course, A_CourseOffering, A_Schedule
from schedule.utils import create_default_section


def course_to_alg_course(course: Course) -> A_Course:
    try:
        a_course = A_Course.objects.get(code=course.course_code)
    except A_Course.DoesNotExist:
        a_course = A_Course()
    a_course.title = course.course_title,
    a_course.pengRequired = course.pengRequired,
    a_course.yearRequired = course.yearRequired
    a_course.save()
    return a_course


def course_to_course_offering(course: Course) -> A_CourseOffering:
    a_course = course_to_alg_course(course)
    course_offering, _ = A_CourseOffering.objects.get_or_create(course=a_course)
    if len(course_offering.sections.all()) == 0:
        course_offering.save()
        a01 = create_default_section()
        a01.save()
        a02 = create_default_section()
        a02.save()
        course_offering.sections.set([a01, a02])
    return course_offering


def add_course_offering_to_schedule(course: Course, a_course_offering: A_CourseOffering):
    schedule = A_Schedule.objects.first()
    if schedule is None:
        print("Adapter ERROR: NO DATABASE DATA FOUND. HAVE YOU RUN init_db.sh?")
        return None

    if course.fall_offering:
        schedule.fall.add(a_course_offering)
    if course.spring_offering:
        schedule.spring.add(a_course_offering)
    if course.summer_offering:
        schedule.summer.add(a_course_offering)
    # TODO: if not course.fall_offering:
    #   schedule.fall.remove(a_course_offering)
    schedule.save()
