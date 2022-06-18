from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
from django.http import HttpResponse
from django.http import HttpRequest
from schedule.views import Schedule


class ViewTest(TestCase):

    def test_GET(self):
        request_factory = APIRequestFactory()
        request: HttpRequest = request_factory.get('/api/schedule/', )
        response: HttpResponse = Schedule().get(request, 2023, "FALL", 2)
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 algorithm")

    def test_POST(self):
        request_factory = APIRequestFactory()
        request: HttpRequest = request_factory.post('/api/schedule/', )
        response: HttpResponse = Schedule().post(request, "sched_id_1", "course_id_1", 2)
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 algorithm")

    def test_GET_scheduleId(self):
        request_factory = APIRequestFactory()
        request: HttpRequest = request_factory.get('/api/schedule/', )
        response: HttpResponse = Schedule().get_schedule_id(request, "sched_id_1", 2)
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 algorithm")
