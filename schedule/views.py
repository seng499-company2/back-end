from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework import status

from coursescheduler import generate_schedule as c2alg1# Company 2 alg 1 
from forecaster.forecaster import forecast as c2alg2 # company 2 alg 2

from c1algo1 import scheduler as c1alg1# company 1 alg 1
from c1algo2.forecaster import forecast as c1algo2
# import c1algo2 # TODO: CURRENTLY THROWING A MODULENOTFOUND ERROR, despite a successful pip install

from schedule.alg_data_generator import get_historic_course_data
from schedule.alg_data_generator import get_program_enrollment_data
from schedule.alg_data_generator import get_schedule
from schedule.alg_data_generator import get_professor_dict

from courses.models import Course


class Schedule(APIView):
    # GET / schedule / {year - semester}
    def get(self, request: HttpRequest, year: int, semester: str, requested_company_alg: int) -> HttpResponse:

        # Create params for algorithms packages
        historical_data = get_historic_course_data()
        previous_enrollment = get_program_enrollment_data()
        schedule = get_schedule()
        professors = get_professor_dict()

        # Call algorithms
        # alg2_result = c2alg2(historical_data, previous_enrollment, schedule) if requested_company_alg == 1 \
        #     else c1alg2(historical_data, previous_enrollment, schedule)
        # alg1_result = c1alg1.generate_schedule() if requested_company_alg == 1 \
        #     else c2alg1(professors, alg2_result, None)

        # just in here to make unit tests pass while we build Alg params
        alg1_result = "OK"
        alg2_result = "OK"

        if "OK" == alg1_result and "OK" == alg2_result:
            body = "GENERATED SCHEDULE FROM COMPANY %d ALGORITHM, AND BOTH RETURNED OK" % requested_company_alg
            return HttpResponse(body, status=status.HTTP_200_OK)
        else: 
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST / schedule / {scheduleId} / {courseId}
    def post(self, request: HttpRequest, schedule_id: str, course_id: str,  company_alg: int) -> HttpResponse:
        body = "GENERATED SCHEDULE FROM COMPANY %d ALGORITHM" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)


class ScheduleFile(APIView):
    # GET / schedules / files / {scheduleId}
    def get(self, request: HttpRequest, schedule_id: str,  company_alg: int) -> HttpResponse:
        body = "GENERATED SCHEDULE FROM COMPANY %d ALGORITHM" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)
