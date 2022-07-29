import typing
import json
import pickle
from preferences.models import Preferences
from schedule.Schedule_models import A_Schedule
from schedule.Schedule_serializers import A_ScheduleSerializer, A_Company1ScheduleSerializer
from users.models import AppUser


def get_historic_course_data() -> typing.Dict[str, str]:
    with open("resources/historicCourseData.json") as json_file:
        return json.load(json_file)


def get_program_enrollment_data() -> typing.Dict[str, str]:
    with open("resources/programEnrollmentData.json") as json_file:
        return json.load(json_file)


def get_schedule(company: int):
    schedule = A_Schedule.objects.first()
    if schedule is None:
        print("Alg Generator ERROR: NO DATABASE DATA FOUND. HAVE YOU RUN init_db.sh?")
        raise FileNotFoundError
    schedule_serializer = A_Company1ScheduleSerializer(instance=schedule) if company == 1 \
        else A_ScheduleSerializer(instance=schedule)
    data = schedule_serializer.data
    return json.loads(json.dumps(data))


# difficulty: 1 = able, 2 = with effort, 0 = no selection
# willingness: 1 = unwilling, 2 = willing, 3 = very willing, 0 = no selection

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


def calculate_teaching_obligations(faculty_type, sebatical_length):
   
    if faculty_type == 'RP' and sebatical_length == 'FULL':
        teaching_obligations = 0
    elif faculty_type == 'RP' and sebatical_length == 'HALF':
        teaching_obligations = 1
    elif faculty_type == 'RP' and sebatical_length == 'NONE':
        teaching_obligations = 3
    elif faculty_type == 'TP' and sebatical_length == 'FULL':
        teaching_obligations = 2
    elif faculty_type == 'TP' and sebatical_length == 'HALF':
        teaching_obligations = 3
    elif faculty_type == 'TP' and sebatical_length == 'NONE':
        teaching_obligations = 6

    return teaching_obligations

def update_course_preferences(course_preferences):
    coursePreferences = []
    for course, values in course_preferences.items():
        preference = {}
        preference['courseCode'] = course
        preference['enthusiasmScore'] = calculate_enthusiasm_score(values['difficulty'],values['willingness'])
        coursePreferences.append(preference)
    return coursePreferences


#merges Preferences.preferredTimes time intervals by joining distinct tuples on their boundaries
def merge_preferred_times(unmerged_preferred_times):
    merged_times = {
        "fall": {},
        "spring": {},
        "summer": {}
    }

    for semester in unmerged_preferred_times:
        #handle edge case where some semester may not have any preferredTimes - must set to None
        if not unmerged_preferred_times[semester]:
            merged_times[semester] = None
            continue

        for key in unmerged_preferred_times[semester]:
            unmerged_list = unmerged_preferred_times[semester][key]

            #merge all timeranges for the weekday
            i = 0
            while i < len(unmerged_list) - 1:
                t1start, t1end = unmerged_list[i]
                j = i+1
                while j < len(unmerged_list):
                    t2start, t2end = unmerged_list[j]
                    if t1end == t2start:
                        unmerged_list[i] = [t1start, t2end]
                        t1end = t2end
                        unmerged_list.pop(j)
                    else:
                        j += 1
                i += 1

            #set the merged timeranges as the value of the dict key
            merged_list = unmerged_list
            merged_times[semester][key] = merged_list

    return merged_times
    

def get_professor_dict():
    preferences: [Preferences] = Preferences.objects.all()
    professors: [] = []
    for preference in preferences:
        if preference.is_submitted:
            appUser: AppUser = preference.professor
            prof_dict = {}
            prof_dict["id"] = str(appUser.user.id)
            prof_dict["name"] = appUser.user.first_name + ' ' + appUser.user.last_name
            prof_dict["isPeng"] = appUser.is_peng
            prof_dict["facultyType"] = "RESEARCH" if appUser.prof_type == "RP" else "TEACHING"
            prof_dict["coursePreferences"] = update_course_preferences(preference.courses_preferences)
            prof_dict["teachingObligations"] = calculate_teaching_obligations(appUser.prof_type, preference.sabbatical_length)

            #merge the preferredTimes prior to setting it in the Preferences object, for the Algorithms teams
            prof_dict["preferredTimes"] = merge_preferred_times(preference.preferred_times)
            prof_dict["preferredNonTeachingSemester"] = preference.preferred_non_teaching_semester.upper()
            if prof_dict["preferredNonTeachingSemester"] == "":
                prof_dict["preferredNonTeachingSemester"] = None
            prof_dict["preferredCoursesPerSemester"] = preference.preferred_courses_per_semester
            prof_dict["preferredCourseDaySpreads"] = preference.preferred_course_day_spreads
            professors.append(prof_dict)
    return professors


def get_professor_dict_mock():
    with open("resources/professor_object_(alg1_input).json") as json_file:
        return json.load(json_file)


def get_professor_object_company1():
    prof_data = open("resources/professors_updated", 'rb')
    professors = pickle.load(prof_data)
    return professors


def get_schedule_error():
    with open("resources/schedule_object_error_case.json") as json_file:
        return json.load(json_file)


def get_profs_error():
    with open("resources/professor_object_error_case.json") as json_file:
        return json.load(json_file)
