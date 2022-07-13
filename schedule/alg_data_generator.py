import typing
import json
import pickle
from courses.models import Course
from users.models import AppUser
from preferences.models import Preferences
from schedule.adapter import course_to_alg_dictionary, course_to_alg_course, a_course_offering_to_dict
from schedule.Schedule_models import A_Course, A_CourseOffering, A_Schedule, A_TimeSlot, A_CourseSection
from schedule.utils import create_default_section


def get_historic_course_data() -> typing.Dict[str, str]:
    with open("resources/historicCourseData.json") as json_file:
        return json.load(json_file)


def get_program_enrollment_data() -> typing.Dict[str, str]:
    with open("resources/programEnrollmentData.json") as json_file:
        return json.load(json_file)


def get_schedule():
    courses = Course.objects.all()
    align_all_courses(courses)
    fall_courses: [Course] = list(filter(lambda course: course.fall_offering, courses))
    spring_courses: [Course] = list(filter(lambda course: course.spring_offering, courses))
    summer_courses: [Course] = list(filter(lambda course: course.summer_offering, courses))
    fall_course_offerings: [A_CourseOffering] = get_course_offerings(fall_courses)
    spring_course_offerings: [A_CourseOffering] = get_course_offerings(spring_courses)
    summer_course_offerings: [A_CourseOffering] = get_course_offerings(summer_courses)
    fall_course_offerings_dict = list(map(a_course_offering_to_dict, fall_course_offerings))
    spring_course_offerings_dict = list(map(a_course_offering_to_dict, spring_course_offerings))
    summer_course_offerings_dict = list(map(a_course_offering_to_dict, summer_course_offerings))
    schedule = {"fall": fall_course_offerings_dict,
                "spring": spring_course_offerings_dict,
                "summer": summer_course_offerings_dict
                }
    return schedule


def align_all_courses(courses: [Course]):
    courses = list(map(course_to_alg_course, courses))
    map((lambda alg_course: alg_course.save), courses)


def get_course_offerings(courses):
    course_offerings: [A_CourseOffering] = A_CourseOffering.objects.all()
    a_course_offerings_filtered = []
    for course_offering in course_offerings:
        # checks if the course offering's course is in the list of courses passed in as a param
        # so courses with fall course offerings end up in the fall_course_offerings list
        a_course = course_offering.course
        for course in courses:
            if a_course is not None and a_course.code == course.course_code:
                a_course_offerings_filtered.append(course_offering)

    if len(courses) == len(a_course_offerings_filtered):
        # Every course already has a course offering, no problems!
        return a_course_offerings_filtered

    # Create course offerings for courses without course offerings
    courses_without_offerings = []
    for course in courses:
        for course_offering in a_course_offerings_filtered:
            if course.course_code == course_offering.course:
                break
        courses_without_offerings.append(course)

    # Create course offerings for courses without offerings
    for course in courses_without_offerings:
        a_course_offerings_filtered.append(create_course_offering(course))
    return a_course_offerings_filtered


def create_course_offering(course: Course):
    a_course_offering: A_CourseOffering = A_CourseOffering()
    a_course_offering.course = course_to_alg_course(course)
    a_course_offering.course.save()

    default_A01_section = create_default_section()
    default_A02_section = create_default_section()

    # create default time slots
    default_time_section, _ = A_TimeSlot.objects.get_or_create(dayOfWeek='', timeRange=['', ''])
    default_time_section.save()

    # add timeslots
    default_A01_section.timeSlots.set([default_time_section])
    default_A02_section.timeSlots.set([default_time_section])
    default_A01_section.save()
    default_A02_section.save()

    # save course offering then set the sections
    # both must be saved before .sections.set() is called
    a_course_offering.save()
    a_course_offering.sections.set([default_A01_section, default_A02_section])
    a_course_offering.save()
    return a_course_offering


def get_professor_dict():
    preferences: [Preferences] = Preferences.objects.all()
    professors: [] = []
    for preference in preferences:
        user: AppUser = preference.professor
        prof_dict = {}
        prof_dict["id"] = user.id
        prof_dict["isPeng"] = user.is_peng
        prof_dict["facultyType"] = user.prof_type
        prof_dict["coursePreferences"] = None # TODO: Does that exist?
        prof_dict["teachingObligations"] = 3 if user.prof_type == "RP" else 6 # TODO: verify accuracy of calculation
        prof_dict["preferredTimes"] = preference.preferred_hours
        prof_dict["preferredCoursesPerSemester"] = preference.teaching_willingness  # TODO: Does that exist?
        preferred_non_teaching_semester = None
        if preference.is_unavailable_sem1:
            preferred_non_teaching_semester = "FALL"
        elif preference.is_unavailable_sem2:
            preferred_non_teaching_semester = "SPRING"
        elif preference.is_unavailable_sem3:
            preferred_non_teaching_semester = "SUMMER"
        prof_dict["preferredNonTeachingSemester"] = preferred_non_teaching_semester
        prof_dict["preferredCourseDaySpreads"] = None # TODO: Does that exist?
        professors.append(prof_dict)
    return professors


def get_professor_dict_mock():
    with open("resources/professor_object_(alg1_input).json") as json_file:
        return json.load(json_file)


def get_schedule_alg1_mock():
    with open("resources/schedule_object_capacities_(alg1_input).json") as json_file:
        return json.load(json_file)


def get_schedule_alg2_mock():
    with open("resources/schedule_object_no_capacities_(alg2_input).json") as json_file:
        return json.load(json_file)


def get_professor_object_company1():
    prof_data = open("resources/professors_updated", 'rb')
    professors = pickle.load(prof_data)
    return professors


def get_schedule_object_company1():
    schedule_data = open("resources/schedule_updated", 'rb')
    schedule = pickle.load(schedule_data)
    return schedule


def get_schedule_error():
    with open("resources/schedule_object_error_case.json") as json_file:
        return json.load(json_file)


def get_profs_error():
    with open("resources/professor_object_error_case.json") as json_file:
        return json.load(json_file)
