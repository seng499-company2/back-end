from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User
from schedule.adapter import course_to_alg_dictionary, course_to_alg_course, a_course_offering_to_dict
from courses.models import Course
from schedule.alg_data_generator import get_historic_course_data, get_program_enrollment_data, get_schedule
from schedule.Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering
from schedule.Schedule_serializers import A_ScheduleSerializer


class ViewTest(TestCase):


    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
        self.client: APIClient = APIClient()
        token = SlidingToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.maxDiff = None

    def init_course(self):
        try:
            self.course = Course.objects.get(course_code="SENG499")
        except:
            self.course_attributes = {
                "course_code": "SENG499",
                "num_sections": 2,
                "course_title": "Design Project 2",
                "fall_offering": True,
                "spring_offering": True,
                "summer_offering": True,
                "pengRequired": {"fall": True, "spring": True, "summer": True},
                "yearRequired": 4
            }
            self.course = Course.objects.create(**self.course_attributes)

    def get_one_course_dict(self):
        expected = \
            {"course":
                {
                    "code": "SENG499",
                    "title": "Design Project 2",
                    "pengRequired": {
                        "fall": True,
                        "spring": True,
                        "summer": True
                    },
                    "yearRequired": 4
                },
                "sections": [
                    {
                        "professor": "",
                        "capacity": 0,
                        "timeslots": []
                    },
                    {
                        "professor": "",
                        "capacity": 0,
                        "timeslots": []
                    },
                ]
            }
        return expected

# IGNORE to ignore test while agl2 fixes their bugs
    def IGNORE_test_GET_company_1(self):
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

# IGNORE to ignore test while agl2 fixes their bugs
    def IGNORE_test_GET_company_2(self):
        response = self.client.get('/schedule/2022/FALL/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_GET_company_2_error(self):
        response = self.client.get('/schedule/2022/FALL/2?use_mock_data=true', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

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

    def test_trivial_course_to_alg_dict(self):
        self.init_course()
        course = self.course
        course_dict = course_to_alg_dictionary(course)
        self.assertIsNotNone(course_dict)
        self.assertEquals("SENG499", course_dict["code"])
        self.assertEquals("Design Project 2", course_dict["title"])
        self.assertEquals(True, course_dict["pengRequired"]["fall"])
        self.assertEquals(4, course_dict["yearRequired"])
        try:
            state = course_dict["_state"]
            # Should have thrown keyError
            self.fail()
        except KeyError:
            # expected behaviour is throwing a KeyError
            pass

    def test_a_course_offering_to_dict(self):
        self.init_course()
        a_course_offering: A_CourseOffering = A_CourseOffering()
        a_course_offering.course = course_to_alg_course(self.course)
        a_course_offering.course.save()

        # create defaut sections
        default_A01_section = A_CourseSection()
        default_A01_section.professor = ''
        default_A01_section.capacity = 0
        default_A01_section.save()
        default_A02_section = A_CourseSection()
        default_A02_section.professor = ''
        default_A02_section.capacity = 0
        default_A02_section.save()

        # create default time slots
        default_time_section = A_TimeSlot()
        default_time_section.dayOfWeek = ''
        default_time_section.timeRange = ['', '']
        default_time_section.save()

        # add timeslots
        default_A01_section.timeSlots.set([default_time_section])
        default_A02_section.timeSlots.set([default_time_section])

        default_A01_section.save()
        default_A02_section.save()
        a_course_offering.save()
        a_course_offering.sections.set([default_A01_section, default_A02_section])
        a_course_offering.save()
        expected = self.get_one_course_dict()
        self.assertDictEqual(expected, a_course_offering_to_dict(a_course_offering))


# alg2_data_generator TESTS

    def test_historic_course_data(self):
        historic_data_dict = get_historic_course_data()
        self.assertEquals(4831, len(historic_data_dict))

    def test_program_enrollment_data(self):
        historic_data_dict = get_program_enrollment_data()
        self.assertEquals(8, len(historic_data_dict))

    def test_get_schedule_no_courses(self):
        schedule = get_schedule()
        expected = {"fall": [], "spring": [], "summer": []}
        self.assertDictEqual(expected, schedule)

    def test_get_schedule_one_course(self):
        self.init_course()
        schedule = get_schedule()
        expected_course_offering = self.get_one_course_dict()
        expected = {'fall': [expected_course_offering], 'spring': [expected_course_offering], 'summer': [expected_course_offering]}
        self.assertDictEqual(expected, schedule)

    def test_get_schedule_many_courses(self):
        # TODO
        schedule = get_schedule()
        expected = {"fall": [], "spring": [], "summer": []}
        self.assertEquals(expected, schedule)
