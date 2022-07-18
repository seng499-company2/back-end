import typing

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from preferences.models import Preferences
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User
from schedule.adapter import add_course_offering_to_schedule, course_to_course_offering
from courses.models import Course
from schedule.alg_data_generator import get_historic_course_data, get_program_enrollment_data, \
    get_schedule, get_professor_dict
from collections import OrderedDict

from users.models import AppUser
from users.serializers import AppUserSerializer

quick_test_mode = False

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
        except Course.DoesNotExist:
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
            self.course.save()
        alg_course_offering = course_to_course_offering(self.course)
        add_course_offering_to_schedule(self.course, alg_course_offering)

    def init_course2(self):
        try:
            self.course = Course.objects.get(course_code="SENG321")
        except Course.DoesNotExist:
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
            alg_course_offering = course_to_course_offering(self.course2)
            add_course_offering_to_schedule(self.course, alg_course_offering)

    def get_course1_ordered_dict(self):
        expected = OrderedDict()
        expected_course = OrderedDict()
        expected_course["code"] = "SENG499"
        expected_course["title"] = "Design Project 2"
        expected_course["pengRequired"] = {"fall": True, "spring": True, "summer": True}
        expected_course["yearRequired"] = 4
        expected_section1 = OrderedDict()
        expected_section1["professor"] = ""
        expected_section1["capacity"] = 0
        expected_section1["timeSlots"] = []
        expected["course"] = expected_course
        expected["sections"] = [expected_section1, expected_section1]
        return expected

    def get_course1_dict(self):
        expected = \
            {"course":
                {
                    "code": "SENG499",
                    "title": "Design Project 2",
                    "pengRequired": {"fall": True, "spring": True, "summer": True},
                    "yearRequired": 4
                },
                "sections": [
                    {
                        "professor": None,
                        "capacity": 0,
                        "timeSlots": []
                    },
                    {
                        "professor": None,
                        "capacity": 0,
                        "timeSlots": []
                    },
                ]
            }
        return expected

    def get_course2_dict(self):
        expected = {}
        expected_course = {"code": "SENG321", "title": "Requirements Engineering",
                           "pengRequired": {"fall": False, "spring": False, "summer": False}, "yearRequired": 3}
        expected_section1 = {"professor": None, "capacity": 0, "timeSlots": []}
        expected["course"] = expected_course
        expected["sections"] = [expected_section1, expected_section1]
        return expected

    def test_GET_company_1_no_courses(self):
        if quick_test_mode:
            return
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

    def test_GET_company_2_no_courses(self):
        if quick_test_mode:
            return
        response = self.client.get('/schedule/2022/FALL/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_GET_company_2_two_courses(self):
        if quick_test_mode:
            return
        self.init_course1()
        self.init_course2()
        response = self.client.get('/schedule/2022/FALL/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_GET_company_1_two_courses(self):
        if quick_test_mode:
            return
        self.init_course1()
        self.init_course2()
        response = self.client.get('/schedule/2022/FALL/1', format='json')
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
        expected_course_offering: typing.Dict = self.get_course1_dict()
        expected = {}
        expected["fall"] = [expected_course_offering]
        expected["spring"] = [expected_course_offering]
        expected["summer"] = [expected_course_offering]
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

class GetProfessorDictTest(TestCase):
    @classmethod
    def setUp(self): 
        self.maxDiff = None
        #build AppUser instance
        self.user_attributes = {
            'username': 'johnd1',
            'password': 'securepass2',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johnd123@uvic.ca',
            'is_superuser': False
        }
        self.user = User.objects.create_user(**self.user_attributes)

        self.app_user_attributes = {
            'user': self.user,
            'prof_type': 'TP',
            'is_peng': False,
            'is_form_submitted': True
        }
        self.app_user = AppUser.objects.create(**self.app_user_attributes)
        self.app_user_serializer = AppUserSerializer(instance=self.app_user)

        #create associated Preferences record
        self.preferences_attributes = {
            "professor": self.app_user,
            "is_submitted": True,
            "taking_sabbatical": True,
            "sabbatical_length": "HALF",
            "sabbatical_start_month": 5,
            "preferred_times": {
                "fall": {
                        "monday": [
                              ["8:30", "18:30" ],
                              ["19:30", "20:30"]
                        ],
                        "tuesday": [
                              ["8:30", "18:30"]
                        ],
                        "wednesday": [
                              ["8:30", "18:30"]
                        ],
                        "thursday": [
                              ["8:30", "18:30"]
                        ],
                        "friday": [
                              ["8:30", "18:30"]
                        ]
                  },
                  "spring": {
                        "monday": [],
                        "tuesday": [
                              ["8:30", "18:30"]
                        ],
                        "wednesday": [
                              ["8:30", "18:30"]
                        ],
                        "thursday": [
                              ["8:30", "18:30"]
                        ],
                        "friday": [
                              ["8:30","18:30"]
                        ]
                  },
                  "summer": {}
            },
            "courses_preferences": {
                    "CSC111": {
                        "willingness": 2,
                        "difficulty": 1
                    },
                    "CSC115": {
                        "willingness": 1,
                        "difficulty": 2
                    }
            },
            "preferred_non_teaching_semester": "summer",
            "preferred_courses_per_semester": {
                  "fall": 2,
                  "spring": 1,
                  "summer": 0
            },

            "preferred_course_day_spreads": [
                   "TWF", "T", "W", "F" 
            ],
        }
        
        Preferences.objects.update(**self.preferences_attributes)

        
    def test_get_professor_dict(self):
        result = get_professor_dict()
        
        expected = {
            "id": str(self.user.id),
            "name": "John Doe",
            "isPeng": False,
            "facultyType": "TEACHING",
            "teachingObligations": 3,
            "coursePreferences": [
                  {
                        "courseCode": "CSC111",
                        "enthusiasmScore": 78
                  },
                  {
                        "courseCode": "CSC115",
                        "enthusiasmScore": 20
                  },
            ],
            "preferredTimes": {
                  "fall": {
                        "monday": [
                              ["8:30", "18:30" ],
                              ["19:30", "20:30"]
                        ],
                        "tuesday": [
                              ["8:30", "18:30"]
                        ],
                        "wednesday": [
                              ["8:30", "18:30"]
                        ],
                        "thursday": [
                              ["8:30", "18:30"]
                        ],
                        "friday": [
                              ["8:30", "18:30"]
                        ]
                  },
                  "spring": {
                        "monday": [],
                        "tuesday": [
                              ["8:30", "18:30"]
                        ],
                        "wednesday": [
                              ["8:30", "18:30"]
                        ],
                        "thursday": [
                              ["8:30", "18:30"]
                        ],
                        "friday": [
                              ["8:30","18:30"]
                        ]
                  },
                  "summer": {}
            },
            "preferredCoursesPerSemester": {
                  "fall": 2,
                  "spring": 1,
                  "summer": 0
            },
            "preferredNonTeachingSemester": "SUMMER",
            "preferredCourseDaySpreads": [
                  "TWF", "T", "W", "F" 
            ]
        }
        self.assertEqual(expected, result[0])