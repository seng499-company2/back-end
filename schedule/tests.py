from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
from schedule.views import Schedule
from schedule.views import ScheduleFile
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User


class ViewTest(TestCase):

    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
        self.client: APIClient = APIClient()
        token = SlidingToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_GET(self):
        response = self.client.get('/schedule/2022/FALL/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 ALGORITHM")

    def test_POST(self):
        response = self.client.post('/schedule/schedule_id/course_id/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 ALGORITHM")

    def test_GET_from_scheduleId(self):
        response = self.client.get('/schedule/files/schedule_id/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 ALGORITHM")
