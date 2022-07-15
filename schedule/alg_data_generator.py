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

#difficulty: 1 = able, 2 = with effort, 0 = no selection
#willingness: 1 = unwilling, 2 = willing, 3 = very willing, 0 = no selection

def calculate_enthusiasm_score(difficulty, willingness):

    enthusiasm_score = 0

    if difficulty == 2 and willingness == 1:
        enthusiasm_score = 20
    elif difficulty == 1 and willingness == 1:
        enthusiasm_score = 39
    elif difficulty == 2 and willingness == 2:
        enthusiasm_score = 40
    elif difficulty == 1 and willingness == 2:
        enthusiasm_score = 78
    elif difficulty == 2 and willingness == 3:
        enthusiasm_score = 100
    elif difficulty == 1 and willingness == 3:
        enthusiasm_score = 195

    return enthusiasm_score



def update_course_preferences(course_preferences):
    coursePreferences = []
    for keys, values in course_preferences.items():
        preference = {}
        preference['courseCode'] = keys
        # Update with actual function
        enthusiasmScore = values['willingness'] * values['difficulty']
        preference['enthusiasmScore'] = enthusiasmScore
        coursePreferences.append(preference)
    print(coursePreferences)
    return 0

def update_preferred_times(preferred_times):
    for day in preferred_times['fall']:
        print(day)
    return 0

# take into consideration sabattical
    

def get_professor_dict():
    preferences: [Preferences] = Preferences.objects.all()
    professors: [] = []
    for preference in preferences:
        appUser: AppUser = preference.professor
        prof_dict = {}
        prof_dict["id"] = appUser.user.id
        prof_dict["name"] = appUser.user.first_name + ' ' + appUser.user.last_name
        prof_dict["isPeng"] = appUser.is_peng
        prof_dict["facultyType"] = appUser.prof_type
        prof_dict["coursePreferences"] = update_course_preferences(preference.courses_preferences)
        prof_dict["teachingObligations"] = 3 if appUser.prof_type == "RP" else 6 # TODO: verify accuracy of calculation
        update_preferred_times(preference.preferred_times)
        prof_dict["preferredTimes"] = preference.preferred_times
        prof_dict["preferredCoursesPerSemester"] = preference.preferred_courses_per_semester  
        prof_dict["preferredNonTeachingSemester"] = preference.preferred_non_teaching_semester
        prof_dict["preferredCourseDaySpreads"] = preference.preferred_course_day_spreads
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
