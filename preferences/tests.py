from django.test import TestCase

from django.contrib.auth.models import User
from .models import Preferences
from users.models import AppUser
from .serializers import PreferencesSerializer
from users.serializers import AppUserSerializer


class PreferencesSerializerTest(TestCase):
    @classmethod
    def setUp(self):
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
            'prof_type': 'RP',
            'is_peng': True
        }
        self.app_user = AppUser.objects.create(**self.app_user_attributes)
        self.app_user_serializer = AppUserSerializer(instance=self.app_user)

        #create associated Preferences record
        self.preferences_attributes = {
            "professor": self.app_user,
            "is_submitted": True,
            "is_unavailable_sem1": False,
            "is_unavailable_sem2": True,
            "num_relief_courses": 1,
            "taking_sabbatical": True,
            "sabbatical_length": "FULL",
            "sabbatical_start_month": 1,
            "preferred_hours": [
                {"Mon": "8am-9am"},
                {"Thu": "1pm-2pm"}
            ],
            "teaching_willingness": {
                "CSC226": "Very Willing"
            },
            "teaching_difficulty": {
                "CSC226": "Able"
            },
            "wants_topics_course": True,
            "topics_course_id": "CSC485c",
            "topics_course_name": "Data Management and Parallelization"
        }
        self.preferences_record = Preferences.objects.create(**self.preferences_attributes)
        self.serializer = PreferencesSerializer(instance=self.preferences_record)


    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'professor',
            'is_submitted',
            'is_unavailable_sem1',
            'is_unavailable_sem2',
            'num_relief_courses',
            'taking_sabbatical',
            'sabbatical_length',
            'sabbatical_start_month',
            'preferred_hours',
            'teaching_willingness',
            'teaching_difficulty',
            'wants_topics_course',
            'topics_course_id',
            'topics_course_name']))

    
    def test_professor_field_converts_to_string(self):
        data = self.serializer.data
        self.assertIsInstance(data['professor'], str)