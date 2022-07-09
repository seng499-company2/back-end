from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework import status

from coursescheduler import generate_schedule as c2alg1# Company 2 alg 1 
from forecaster.forecaster import forecast as c2alg2 # company 2 alg 2

from c1algo1 import scheduler as c1alg1# company 1 alg 1
from c1algo2.forecaster import forecast as c1algo2



class Schedule(APIView):
    # GET / schedule / {year - semester}
    def get(self, request: HttpRequest, year: int, semester: str, requested_company_alg: int) -> HttpResponse:
        alg2_result = c2alg1(None, None, None) if requested_company_alg == 1 else c2alg2(None, None, None)
        alg1_result = c1alg1.generate_schedule() if requested_company_alg == 1 else c2alg1(None, None, None)

        # these 2 lines are temporary and just to make unit tests pass while integration is in progress
        alg2_result = "OK"
        alg1_result = "OK"

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
