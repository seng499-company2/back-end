from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User
from schedule.adapter import course_to_dictionary
from courses.models import Course


class ViewTest(TestCase):

    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
        self.client: APIClient = APIClient()
        token = SlidingToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_GET_company_1(self):
        response = self.client.get('/schedule/2022/FALL/1', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 1 ALGORITHM")

    def test_POST_company_1(self):
        response = self.client.post('/schedule/schedule_id/course_id/1', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 1 ALGORITHM")

    def test_GET_from_scheduleId_company_1(self):
        response = self.client.get('/schedule/files/schedule_id/1', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 1 ALGORITHM")

    def test_GET_company_2(self):
        response = self.client.get('/schedule/2022/FALL/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 ALGORITHM")

    def test_POST_company_2(self):
        response = self.client.post('/schedule/schedule_id/course_id/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 ALGORITHM")

    def test_GET_from_scheduleId_company_2(self):
        response = self.client.get('/schedule/files/schedule_id/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, "GENERATED SCHEDULE FROM COMPANY 2 ALGORITHM")

# ADAPTER TESTS
    def test_none(self):
        course_dict = course_to_dictionary(None)
        self.assertIsNone(course_dict)

    def test_trivial(self):
        course_attributes = {
            "course_code": "SENG499",
            "section": "A01",
            "course_title": "Design Project 2",
            "fall_offering": True,
            "spring_offering": True,
            "summer_offering": False,
            "PENG_required": True
        }
        course = Course.objects.create(**course_attributes)
        course_dict = course_to_dictionary(course)
        self.assertIsNotNone(course_dict)
        self.assertEquals("SENG499", course_dict["course_code"])
        self.assertEquals("A01", course_dict["section"])
        self.assertEquals("Design Project 2", course_dict["course_title"])
        self.assertEquals(True, course_dict["fall_offering"])
        self.assertEquals(True, course_dict["spring_offering"])
        self.assertEquals(False, course_dict["summer_offering"])
        self.assertEquals(True, course_dict["PENG_required"])
        try:
            state = course_dict["_state"]
            # Should have thrown keyError
            self.fail()
        except KeyError:
            # expected behaviour is throwing a KeyError
            pass
