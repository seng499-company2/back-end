import typing
import json
from courses.models import Course
from users.models import AppUser
from preferences.models import Preferences
from schedule.adapter import course_to_alg_dictionary


def get_historic_course_data() -> typing.Dict[str, str]:
    with open("resources/historicCourseData.json") as json_file:
        return json.load(json_file)


def get_program_enrollment_data() -> typing.Dict[str, str]:
    with open("resources/programEnrollmentData.json") as json_file:
        return json.load(json_file)


def get_schedule():
    courses = Course.objects.all()
    fall_courses: [Course] = list(filter(lambda course: course.spring_offering, courses))
    spring_courses: [Course] = list(filter(lambda course: course.spring_offering, courses))
    summer_courses: [Course] = list(filter(lambda course: course.summer_offering, courses))
    fall_course_offerings = get_course_offerings(fall_courses)
    spring_course_offerings = get_course_offerings(spring_courses)
    summer_course_offerings = get_course_offerings(summer_courses)
    schedule = {"fall": fall_course_offerings,
                "spring": spring_course_offerings,
                "summer": summer_course_offerings
                }
    print(schedule)
    return schedule


def get_course_offerings(courses):
    alg_course_dicts = list(map(course_to_alg_dictionary, courses))
    course_offerings = []
    for alg_course_dict in alg_course_dicts:
        section1 = {"professor": "", "capacity": "", "timeslots": ""}
        section2 = {"professor": "", "capacity": "", "timeslots": ""}
        course_offering = {"course": alg_course_dict, "sections": [section1, section2]}
        course_offerings.append(course_offering)
    return course_offerings


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
