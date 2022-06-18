from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework import status
# TODO: import alg 1 and 2 packages from company 1
# TODO: import alg 1 and 2 packages from company 2


class Schedule(APIView):
    # GET / schedule / {year - semester}
    def get(self, request: HttpRequest, year: int, semester: str, company_alg: int) -> HttpResponse:
        body = "GENERATED SCHEDULE FROM COMPANY %d algorithm" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)

    # POST / schedule / {scheduleId} / {courseId}
    def post(self, request: HttpRequest, schedule_id: str, course_id: str,  company_alg: int) -> HttpResponse:
        body = "GENERATED SCHEDULE FROM COMPANY %d algorithm" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)

    # GET / schedules / files / {scheduleId}
    def get_schedule_id(self, request: HttpRequest, schedule_id: str,  company_alg: int) -> HttpResponse:
        body = "GENERATED SCHEDULE FROM COMPANY %d algorithm" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)
