from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User
from schedule.adapter import course_to_alg_dictionary
from courses.models import Course
from schedule.alg_data_generator import get_historic_course_data
from schedule.alg_data_generator import get_program_enrollment_data


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

    def test_POST_company_1(self):
        response = self.client.post('/schedule/schedule_id/course_id/1', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_GET_from_scheduleId_company_1(self):
        response = self.client.get('/schedule/files/schedule_id/1', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_GET_company_2(self):
        response = self.client.get('/schedule/2022/FALL/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_POST_company_2(self):
        response = self.client.post('/schedule/schedule_id/course_id/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_GET_from_scheduleId_company_2(self):
        response = self.client.get('/schedule/files/schedule_id/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

# ADAPTER TESTS
    def test_none(self):
        course_dict = course_to_alg_dictionary(None)
        self.assertIsNone(course_dict)

    def test_trivial(self):
        course_attributes = {
            "course_code": "SENG499",
            "num_sections": 2,
            "course_title": "Design Project 2",
            "fall_offering": True,
            "spring_offering": True,
            "summer_offering": False,
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4
        }
        course = Course.objects.create(**course_attributes)
        course_dict = course_to_alg_dictionary(course)
        self.assertIsNotNone(course_dict)
        self.assertEquals("SENG499", course_dict["code"])
        self.assertEquals("Design Project 2", course_dict["title"])
        self.assertEquals(False, course_dict["pengRequired"]["fall"])
        self.assertEquals(4, course_dict["yearRequired"])
        try:
            state = course_dict["_state"]
            # Should have thrown keyError
            self.fail()
        except KeyError:
            # expected behaviour is throwing a KeyError
            pass

# alg2_data_generator TESTS

    def test_historic_course_data(self):
        historic_data_dict = get_historic_course_data()
        self.assertEquals(4831, len(historic_data_dict))

    def test_program_enrollment_data(self):
        historic_data_dict = get_program_enrollment_data()
        self.assertEquals(8, len(historic_data_dict))

    def test_get_schedule(self):
        pass

    def test_get_professor_dict(self):
        pass
