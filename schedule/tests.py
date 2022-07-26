from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from preferences.models import Preferences
from rest_framework_simplejwt.tokens import SlidingToken
from django.contrib.auth.models import User
from schedule.adapter import add_course_offering_to_schedule, \
    course_to_fall_course_offering, course_to_spring_course_offering, course_to_summer_course_offering
from courses.models import Course
from schedule.alg_data_generator import get_historic_course_data, get_program_enrollment_data, \
    get_schedule, get_professor_dict
from users.models import AppUser
from users.serializers import AppUserSerializer
from schedule.Schedule_models import A_CourseSection

quick_test_mode = False

class ViewTest(TestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
        self.client: APIClient = APIClient()
        token = SlidingToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.maxDiff = None

    def get_default_section(self):
        section = A_CourseSection()
        section.professor = {"name": "professor professorPants"}
        section.capacity = 150
        section.maxCapacity = 200
        section.save()
        return section

    def init_course1(self):
        try:
            self.course = Course.objects.get(course_code="SENG499")
        except Course.DoesNotExist:
            course_attributes = {
                "course_code": "SENG499",
                "course_title": "Design Project 2",
                "pengRequired": {"fall": True, "spring": True, "summer": True},
                "yearRequired": 4
            }
            self.course = Course.objects.create(**course_attributes)
            self.course.save()
            self.course.fall_sections.add(self.get_default_section())
            self.course.spring_sections.add(self.get_default_section())
            self.course.summer_sections.add(self.get_default_section())
        alg_course_offering = course_to_fall_course_offering(self.course)
        add_course_offering_to_schedule(alg_course_offering, "fall")
        alg_course_offering = course_to_spring_course_offering(self.course)
        add_course_offering_to_schedule(alg_course_offering, "spring")
        alg_course_offering = course_to_summer_course_offering(self.course)
        add_course_offering_to_schedule(alg_course_offering, "summer")

    def init_course2(self):
        try:
            self.course2 = Course.objects.get(course_code="SENG321")
        except Course.DoesNotExist:
            course_attributes = {
                "course_code": "SENG321",
                "course_title": "Requirements Engineering",
                "pengRequired": {"fall": False, "spring": False, "summer": False},
                "yearRequired": 3
            }
            self.course2 = Course.objects.create(**course_attributes)
            self.course2.save()
            self.course2.spring_sections.add(self.get_default_section())
            self.course2.spring_sections.add(self.get_default_section())
            self.course2.spring_sections.add(self.get_default_section())
        alg_course_offering = course_to_fall_course_offering(self.course2)
        add_course_offering_to_schedule(alg_course_offering, "fall")
        alg_course_offering = course_to_spring_course_offering(self.course2)
        add_course_offering_to_schedule(alg_course_offering, "spring")
        alg_course_offering = course_to_summer_course_offering(self.course2)
        add_course_offering_to_schedule(alg_course_offering, "summer")

    def init_prof(self):
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
            'is_peng': True,
            'is_form_submitted': True
        }
        self.app_user = AppUser.objects.create(**self.app_user_attributes)
        self.app_user_serializer = AppUserSerializer(instance=self.app_user)

        #create associated Preferences record
        self.preferences_attributes = {
            "professor": self.app_user,
            "is_submitted": True,
            "taking_sabbatical": False,
            "sabbatical_length": "NONE",
            "sabbatical_start_month": 0,
            "preferred_times":
                {"fall":
                    {"friday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"]],
                    "monday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"]],
                    "tuesday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"]],
                    "thursday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"]],
                    "wednesday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"]]},
                "spring":
                    {"friday":
                        [["9:00", "10:00"],
                        ["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"],
                        ["17:00", "18:00"],
                        ["18:00", "19:00"]],
                    "monday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"],
                        ["17:00", "18:00"],
                        ["18:00", "19:00"]],
                    "tuesday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"],
                        ["17:00", "18:00"],
                        ["18:00", "19:00"]],
                    "thursday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"]],
                    "wednesday":
                        [["10:00", "11:00"],
                        ["11:00", "12:00"],
                        ["12:00", "13:00"],
                        ["13:00", "14:00"],
                        ["14:00", "15:00"],
                        ["15:00", "16:00"],
                        ["16:00", "17:00"],
                        ["17:00", "18:00"],
                        ["18:00", "19:00"]]},
                "summer": {}
            },
            "courses_preferences": {
                    "SENG321": {
                        "willingness": 2,
                        "difficulty": 1
                    },
                    "SENG499": {
                        "willingness": 3,
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
        self.assertEquals(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

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
        self.assertEquals(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

    def test_GET_company_2_two_courses(self):
        if quick_test_mode:
            return
        self.init_course1()
        self.init_course2()
        self.init_prof()
        response = self.client.get('/schedule/2022/FALL/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

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
        try:
            schedule = get_schedule(2)
            self.fail()  # Should have thrown an error
        except FileNotFoundError:
            pass  # expected behaviour

    def test_get_professor_dict(self):
        self.init_prof()
        result = get_professor_dict()

        #preferredTimes must now be merged correctly
        expected = [{
            "id": str(self.user.id),
            "name": "John Doe",
            "isPeng": True,
            "facultyType": "TEACHING",
            "teachingObligations": 6,
            "coursePreferences": [
                  {
                        "courseCode": "SENG321",
                        "enthusiasmScore": 78
                  },
                  {
                        "courseCode": "SENG499",
                        "enthusiasmScore": 100
                  },
            ],
            "preferredTimes":
                {"fall":
                    {"friday":
                        [["10:00", "17:00"]],
                    "monday":
                        [["10:00", "17:00"]],
                    "tuesday":
                        [["10:00", "17:00"]],
                    "thursday":
                        [["10:00", "17:00"]],
                    "wednesday":
                        [["10:00", "17:00"]]},
                "spring":
                    {"friday":
                        [["9:00", "19:00"]],
                    "monday":
                        [["10:00", "19:00"]],
                    "tuesday":
                        [["10:00", "19:00"]],
                    "thursday":
                        [["10:00", "16:00"]],
                    "wednesday":
                        [["10:00", "19:00"]]},
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
        }]

        self.assertEqual(expected, result)