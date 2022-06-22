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

    
    def test_professor_field_serializes_to_string(self):
        data = self.serializer.data
        self.assertIsInstance(data['professor'], str)


    def test_valid_deserialization(self):
        serialized_data = {
            "professor": "johnd1",
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
        serializer = PreferencesSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())


    def test_create_preferences_obj(self):
        #build a new AppUser instance
        user_attributes = {
            'username': 'julia2',
            'password': 'securepass2',
            'first_name': 'Julia',
            'last_name': 'May',
            'email': 'juliam456@uvic.ca',
            'is_superuser': False
        }
        user = User.objects.create_user(**user_attributes)

        app_user_attributes = {
            'user': user,
            'prof_type': 'RP',
            'is_peng': True
        }
        app_user = AppUser.objects.create(**app_user_attributes)
        app_user_serializer = AppUserSerializer(instance=app_user)

        #create a new Preferences object using the serializer
        serialized_data = {
            "professor": "julia2",
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
        serializer = PreferencesSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

        #use the serializer to create an AppUser record, then assert it has been committed to DB
        preferences_obj = serializer.save()
        self.assertIsNotNone(preferences_obj.pk)


    def test_update_preferences_obj(self):
        #get an existing Preferences object
        preferences_obj = Preferences.objects.get(professor__user__username="johnd1")
        obj_key = preferences_obj.pk

        #update the Preferences record order by referencing an existing instance
        updated_serialized_data = {
            "professor": "johnd1",
            "is_submitted": False,      #updated
            "is_unavailable_sem1": False,
            "is_unavailable_sem2": True,
            "num_relief_courses": 1,
            "taking_sabbatical": True,
            "sabbatical_length": "HALF", #updated
            "sabbatical_start_month": 1,
            "preferred_hours": [
                {"Mon": "10am-11am"}    #updated JSON
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
        serializer = PreferencesSerializer(instance=preferences_obj, data=updated_serialized_data)
        self.assertTrue(serializer.is_valid())
        updated_preferences_obj = serializer.save()
        updated_obj_key = updated_preferences_obj.pk

        #assert that the same instance was updated, and updated as expected
        self.assertEquals(updated_obj_key, obj_key)
        self.assertEquals(Preferences.objects.get(pk=obj_key).is_submitted, updated_serialized_data['is_submitted'])
        self.assertEquals(Preferences.objects.get(pk=obj_key).sabbatical_length, updated_serialized_data['sabbatical_length'])
        self.assertEquals(Preferences.objects.get(pk=obj_key).preferred_hours, updated_serialized_data['preferred_hours'])