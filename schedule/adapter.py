from courses.models import Course
from schedule.Schedule_models import A_Course, A_CourseOffering, A_Schedule


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


def course_to_fall_course_offering(course: Course) -> A_CourseOffering:
    a_course = course_to_alg_course(course)
    sections = course.fall_sections
    return get_course_offering_for_sections(sections, a_course)


def course_to_spring_course_offering(course: Course) -> A_CourseOffering:
    a_course = course_to_alg_course(course)
    sections = course.spring_sections
    return get_course_offering_for_sections(sections, a_course)


def course_to_summer_course_offering(course: Course):
    a_course = course_to_alg_course(course)
    sections = course.summer_sections
    return get_course_offering_for_sections(sections, a_course)


def get_course_offering_for_sections(sections, a_course: A_Course):
    if not sections.all():
        # Course isn't scheduled in the given semester
        # Creating an object with no sections
        course_offering, _ = A_CourseOffering.objects.get_or_create(course=a_course, sections__in=[])
        course_offering.save()
        return course_offering

    try:
        course_offering = A_CourseOffering.objects.filter(course=a_course, sections__in=sections.all()).first()
        if course_offering is None:
            raise A_CourseOffering.DoesNotExist
    except A_CourseOffering.DoesNotExist:
        course_offering = A_CourseOffering()
        course_offering.course = a_course
        course_offering.save()
        course_offering.sections.set(sections.all())
    course_offering.save()
    return course_offering


def add_course_offering_to_schedule(a_course_offering: A_CourseOffering, semester: str):
    schedule: A_Schedule = A_Schedule.objects.first()
    if schedule is None:
        print("Adapter ERROR: NO DATABASE DATA FOUND. HAVE YOU RUN init_db.sh?")
        return None

    if semester not in ["fall", "spring", "summer"]:
        raise NotImplementedError("cannot add a course offering in the semester '" + semester + "'")

    if "fall" == semester:
        # remove any old course offerings with old data
        fall_course_offerings = schedule.fall.all()
        for old_course_offering in fall_course_offerings:
            if old_course_offering.course == a_course_offering.course:
                schedule.fall.remove(old_course_offering)
        schedule.fall.add(a_course_offering)

    if "spring" == semester:
        # remove any old course offerings with old data
        spring_course_offerings = schedule.spring.all()
        for old_course_offering in spring_course_offerings:
            if old_course_offering.course == a_course_offering.course:
                schedule.spring.remove(old_course_offering)
        schedule.spring.add(a_course_offering)

    if "summer" == semester:
        # remove any old course offerings with old data
        summer_course_offerings = schedule.summer.all()
        for old_course_offering in summer_course_offerings:
            if old_course_offering.course == a_course_offering.course:
                schedule.summer.remove(old_course_offering)
        schedule.summer.add(a_course_offering)

    schedule.save()
