from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User
from schedule.adapter import course_to_alg_dictionary
from courses.models import Course
from schedule.alg_data_generator import get_historic_course_data
from schedule.alg_data_generator import get_program_enrollment_data
from schedule.alg_data_generator import get_schedule
from schedule.Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering
from schedule.Schedule_serializers import A_ScheduleSerializer


class ViewTest(TestCase):

    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
        self.client: APIClient = APIClient()
        token = SlidingToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

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

    def test_get_schedule_no_courses(self):
        schedule = get_schedule()
        expected = {"fall": [], "spring": [], "summer": []}
        self.assertDictEqual(expected, schedule)

    def test_get_schedule_one_course(self):
        self.course_attributes = {
            "course_code": "SENG499",
            "num_sections": 2,
            "course_title": "Design Project 2",
            "fall_offering": True,
            "spring_offering": True,
            "summer_offering": True,
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4
        }
        self.course = Course.objects.create(**self.course_attributes)

        schedule = get_schedule()
        expected = {'fall': [{'course': {'code': 'SENG499', 'title': 'Design Project 2', 'pengRequired': {'fall': False, 'spring': True, 'summer': True}, 'yearRequired': 4}, 'sections': [{'professor': '', 'capacity': '', 'timeslots': ''}, {'professor': '', 'capacity': '', 'timeslots': ''}]}], 'spring': [{'course': {'code': 'SENG499', 'title': 'Design Project 2', 'pengRequired': {'fall': False, 'spring': True, 'summer': True}, 'yearRequired': 4}, 'sections': [{'professor': '', 'capacity': '', 'timeslots': ''}, {'professor': '', 'capacity': '', 'timeslots': ''}]}], 'summer': [{'course': {'code': 'SENG499', 'title': 'Design Project 2', 'pengRequired': {'fall': False, 'spring': True, 'summer': True}, 'yearRequired': 4}, 'sections': [{'professor': '', 'capacity': '', 'timeslots': ''}, {'professor': '', 'capacity': '', 'timeslots': ''}]}]}
        self.assertDictEqual(expected, schedule)

    def test_get_schedule_many_courses(self):
        saved_schedule = self.get_schedule_object()
        schedule = get_schedule()
        expected = {}
        self.assertEquals(expected, schedule)


    def get_schedule_object(self):
        #build TimeSlot objects
        t1 = A_TimeSlot(dayOfWeek='MONDAY', timeRange='("12:00","13:00")')
        t2 = A_TimeSlot(dayOfWeek='TUESDAY', timeRange='("14:00","15:00")')
        t1.save()   #NOTE: Many-to-many relationships cannot be created without saving BOTH entity objects first
        t2.save()

        #build CourseSection objects
        cs1 = A_CourseSection(professor={"id": "mzastre", "name":"Michael Zastre"}, capacity=0)
        cs1.save()
        cs1.timeSlots.add(t1, t2)

        #build Course objects
        c1 = A_Course(code="CSC225", title="Algorithms and Data Structures I", pengRequired={"fall": True, "spring": False, "summer": True}, yearRequired=3)
        c1.save()

        #build CourseOffering objects
        co_fall = A_CourseOffering()
        co_fall.save()
        co_fall.course.add(c1)
        co_fall.sections.add(cs1)

        co_spring = A_CourseOffering()
        co_spring.save()
        co_spring.course.add(c1)
        co_spring.sections.add(cs1)

        co_summer = A_CourseOffering()
        co_summer.save()
        co_summer.course.add(c1)
        co_summer.sections.add(cs1)

        #finally, build Schedule object
        schedule = A_Schedule()
        schedule.save()
        schedule.fall.add(co_fall)
        schedule.spring.add(co_spring)
        schedule.summer.add(co_summer)
        schedule.save()
        return schedule
