import typing
import json
import pickle
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
    courses_dict_list = list(map(course_to_alg_dictionary, courses))
    # TODO: format courses_dict_list into properly formatted schedule dictionary
    schedule = courses_dict_list
    return schedule


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
