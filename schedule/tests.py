from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User
from schedule.adapter import course_to_alg_dictionary, course_to_alg_course, a_course_offering_to_dict
from courses.models import Course
from schedule.alg_data_generator import get_historic_course_data, get_program_enrollment_data, \
    get_schedule, get_course_offerings, create_default_section
from schedule.Schedule_models import A_TimeSlot, A_CourseSection, A_CourseOffering


class ViewTest(TestCase):


    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
        self.client: APIClient = APIClient()
        token = SlidingToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.maxDiff = None

    def init_course1(self):
        try:
            self.course = Course.objects.get(course_code="SENG499")
        except:
            course_attributes = {
                "course_code": "SENG499",
                "num_sections": 2,
                "course_title": "Design Project 2",
                "fall_offering": True,
                "spring_offering": True,
                "summer_offering": True,
                "pengRequired": {"fall": True, "spring": True, "summer": True},
                "yearRequired": 4
            }
            self.course = Course.objects.create(**course_attributes)

    def init_course2(self):
        try:
            self.course = Course.objects.get(course_code="SENG321")
        except:
            course_attributes = {
                "course_code": "SENG321",
                "num_sections": 2,
                "course_title": "Requirements Engineering",
                "fall_offering": True,
                "spring_offering": True,
                "summer_offering": True,
                "pengRequired": {"fall": False, "spring": False, "summer": False},
                "yearRequired": 3
            }
            self.course2 = Course.objects.create(**course_attributes)

    def get_course1_dict(self):
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

    def get_course2_dict(self):
        expected = \
            {"course":
                {
                    "code": "SENG321",
                    "title": "Requirements Engineering",
                    "pengRequired": {
                        "fall": False,
                        "spring": False,
                        "summer": False
                    },
                    "yearRequired": 3
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
        self.init_course1()
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
        self.init_course1()
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
        expected = self.get_course1_dict()
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
        self.init_course1()
        schedule = get_schedule()
        expected_course_offering = self.get_course1_dict()
        expected = {'fall': [expected_course_offering], 'spring': [expected_course_offering], 'summer': [expected_course_offering]}
        self.assertDictEqual(expected, schedule)

    def test_get_schedule_many_courses(self):
        self.init_course1()
        self.init_course2()
        expected_course_offering = self.get_course1_dict()
        expected_course_offering2 = self.get_course2_dict()
        expected = {'fall': [expected_course_offering, expected_course_offering2],
                    'spring': [expected_course_offering, expected_course_offering2],
                    'summer': [expected_course_offering, expected_course_offering2]}

        schedule = get_schedule()
        self.assertEquals(expected, schedule)

    def test_get_course_offerings_no_courses(self):
        a = get_course_offerings([])
        self.assertEquals([], a)

    def test_get_course_offerings_one_course(self):
        self.init_course1()
        actual_course_offering = get_course_offerings([self.course])
        expected_a_course_offering = A_CourseOffering()
        expected_course = course_to_alg_course(self.course)
        expected_a_course_offering.course = expected_course
        expected_a_course_offering.save()
        expected_section_1 = create_default_section()
        expected_section_2 = create_default_section()
        expected_sections = [expected_section_1, expected_section_2]
        expected_a_course_offering.sections.set(expected_sections)
        self.assertEquals(1, len(actual_course_offering))
        self.assertEquals(expected_course, actual_course_offering[0].course)
        i = 0
        for section in actual_course_offering[0].sections.all():
            self.assertEquals(expected_sections[i].professor, section.professor)
            self.assertEquals(expected_sections[i].capacity, section.capacity)
            i += 1

    def test_get_course_offerings_many_courses(self):
        self.init_course1()
        self.init_course2()
        actual_course_offering = get_course_offerings([self.course, self.course2])
        expected_a_course_offering1 = A_CourseOffering()
        expected_a_course_offering2 = A_CourseOffering()
        expected_course1 = course_to_alg_course(self.course)
        expected_course2 = course_to_alg_course(self.course2)
        expected_a_course_offering1.course = expected_course1
        expected_a_course_offering2.course = expected_course2
        expected_a_course_offering1.save()
        expected_a_course_offering2.save()
        expected_section_1 = create_default_section()
        expected_section_2 = create_default_section()
        expected_sections = [expected_section_1, expected_section_2]
        expected_a_course_offering1.sections.set(expected_sections)
        expected_a_course_offering2.sections.set(expected_sections)
        self.assertEquals(2, len(actual_course_offering))
        self.assertEquals(expected_course1, actual_course_offering[0].course)
        self.assertEquals(expected_course2, actual_course_offering[1].course)
        i = 0
        for section in actual_course_offering[0].sections.all():
            self.assertEquals(expected_sections[i].professor, section.professor)
            self.assertEquals(expected_sections[i].capacity, section.capacity)
            i += 1
        i = 0
        for section in actual_course_offering[1].sections.all():
            self.assertEquals(expected_sections[i].professor, section.professor)
            self.assertEquals(expected_sections[i].capacity, section.capacity)
            i += 1
