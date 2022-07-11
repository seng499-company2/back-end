from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework import status

from coursescheduler import generate_schedule as c2alg1# Company 2 alg 1 
from forecaster.forecaster import forecast as c2alg2 # company 2 alg 2

from c1algo1 import scheduler as c1alg1# company 1 alg 1
from c1algo2.forecaster import forecast as c1alg2

from schedule.alg_data_generator import get_historic_course_data
from schedule.alg_data_generator import get_program_enrollment_data
from schedule.alg_data_generator import get_professor_object_company1, get_schedule_alg1_mock, \
    get_professor_dict_mock, get_schedule_alg2_mock

import traceback
import json


class Schedule(APIView):
    # GET / schedule / {year - semester}
    def get(self, request: HttpRequest, year: int, semester: str, requested_company_alg: int) -> HttpResponse:

        # Create params for algorithms packages
        historical_data = get_historic_course_data()
        previous_enrollment = get_program_enrollment_data()
        schedule = get_schedule_alg2_mock()
        professors = get_professor_dict_mock()
        professors_company1 = get_professor_object_company1()

        try:
            alg_2_output = c1alg2(historical_data, previous_enrollment, schedule) if requested_company_alg == 1 \
                 else c2alg2(historical_data, previous_enrollment, schedule)
            if requested_company_alg == 1:
                schedule, error = c1alg1.generate_schedule(professors_company1, alg_2_output)
            else:
                schedule, error = c2alg1(professors, alg_2_output, False)
            if error is not None and error != "":
                return HttpResponse("ERROR WITH ALGORITHMS: " + error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return HttpResponse(json.dumps(schedule), status=status.HTTP_200_OK)
        except Exception as err:
            print(traceback.format_exception(err))
            return HttpResponse("ERROR WITH ALGORITHMS", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST / schedule / {scheduleId} / {courseId}
    def post(self, request: HttpRequest, schedule_id: str, course_id: str,  company_alg: int) -> HttpResponse:
        body = "GENERATED SCHEDULE FROM COMPANY %d ALGORITHM" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)


class ScheduleFile(APIView):
    # GET / schedules / files / {scheduleId}
    def get(self, request: HttpRequest, schedule_id: str,  company_alg: int) -> HttpResponse:
        body = "GENERATED SCHEDULE FROM COMPANY %d ALGORITHM" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)
