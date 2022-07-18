from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from preferences.models import Preferences
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User
from schedule.adapter import course_to_alg_dictionary
from courses.models import Course
from schedule.alg_data_generator import get_historic_course_data
from schedule.alg_data_generator import get_program_enrollment_data, get_professor_dict
from users.models import AppUser
from users.serializers import AppUserSerializer


# class ViewTest(TestCase):

#     @classmethod
#     def setUp(self):
#         user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
#         self.client: APIClient = APIClient()
#         token = SlidingToken.for_user(user)
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

#     def test_GET_company_1(self):
#         response = self.client.get('/schedule/2022/FALL/1', format='json')
#         self.assertIsNotNone(response)
#         self.assertEquals(status.HTTP_200_OK, response.status_code)

#     def test_POST_company_1(self):
#         response = self.client.post('/schedule/schedule_id/course_id/1', format='json')
#         self.assertIsNotNone(response)
#         self.assertEquals(status.HTTP_200_OK, response.status_code)

#     def test_GET_from_scheduleId_company_1(self):
#         response = self.client.get('/schedule/files/schedule_id/1', format='json')
#         self.assertIsNotNone(response)
#         self.assertEquals(status.HTTP_200_OK, response.status_code)

#     def test_GET_company_2(self):
#         response = self.client.get('/schedule/2022/FALL/2', format='json')
#         self.assertIsNotNone(response)
#         self.assertEquals(status.HTTP_200_OK, response.status_code)

#     def test_GET_company_2_error(self):
#         response = self.client.get('/schedule/2022/FALL/2?use_mock_data=true', format='json')
#         self.assertIsNotNone(response)
#         self.assertEquals(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

#     def test_POST_company_2(self):
#         response = self.client.post('/schedule/schedule_id/course_id/2', format='json')
#         self.assertIsNotNone(response)
#         self.assertEquals(status.HTTP_200_OK, response.status_code)

#     def test_GET_from_scheduleId_company_2(self):
#         response = self.client.get('/schedule/files/schedule_id/2', format='json')
#         self.assertIsNotNone(response)
#         self.assertEquals(status.HTTP_200_OK, response.status_code)

# # ADAPTER TESTS
#     def test_none(self):
#         course_dict = course_to_alg_dictionary(None)
#         self.assertIsNone(course_dict)

#     def test_trivial(self):
#         course_attributes = {
#             "course_code": "SENG499",
#             "num_sections": 2,
#             "course_title": "Design Project 2",
#             "fall_offering": True,
#             "spring_offering": True,
#             "summer_offering": False,
#             "pengRequired": {"fall": False, "spring": True, "summer": True},
#             "yearRequired": 4
#         }
#         course = Course.objects.create(**course_attributes)
#         course_dict = course_to_alg_dictionary(course)
#         self.assertIsNotNone(course_dict)
#         self.assertEquals("SENG499", course_dict["code"])
#         self.assertEquals("Design Project 2", course_dict["title"])
#         self.assertEquals(False, course_dict["pengRequired"]["fall"])
#         self.assertEquals(4, course_dict["yearRequired"])
#         try:
#             state = course_dict["_state"]
#             # Should have thrown keyError
#             self.fail()
#         except KeyError:
#             # expected behaviour is throwing a KeyError
#             pass

# # alg2_data_generator TESTS

#     def test_historic_course_data(self):
#         historic_data_dict = get_historic_course_data()
#         self.assertEquals(4831, len(historic_data_dict))

#     def test_program_enrollment_data(self):
#         historic_data_dict = get_program_enrollment_data()
#         self.assertEquals(8, len(historic_data_dict))

#     def test_get_schedule(self):
#         pass

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
        print(result)
        expected = {
            "id": "1",
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