import typing
import json
import pickle
from schedule.Schedule_models import A_Schedule
from schedule.Schedule_serializers import A_ScheduleSerializer


def get_historic_course_data() -> typing.Dict[str, str]:
    with open("resources/historicCourseData.json") as json_file:
        return json.load(json_file)


def get_program_enrollment_data() -> typing.Dict[str, str]:
    with open("resources/programEnrollmentData.json") as json_file:
        return json.load(json_file)


def get_schedule():
    schedule, _ = A_Schedule.objects.get_or_create(id=0)
    schedule_serializer = A_ScheduleSerializer(instance=schedule)
    data = schedule_serializer.data
    return json.loads(json.dumps(data))



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
