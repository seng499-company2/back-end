from django.test import TestCase    #**tests that interact with database require subclassing of this class**

from django.contrib.auth.models import User
from .models import AppUser
from .serializers import AppUserSerializer

#Serializer Testing
class AppUserSerializerTest(TestCase):
    @classmethod
    def setUp(self):
        #build AppUser and AppUserSerializer instances
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
            'prof_type': AppUser.TeachingType.TEACHING_PROF
        }
        #default data for the serializer, if needed
        self.default_serializer_data = {
            'user':{
                'username': 'abcdef',
                'password': '123',
                'first_name': 'Abc',
                'last_name': 'Def',
                'email': 'abc@uvic.ca',
                'is_superuser': False
            },
            'prof_type': AppUser.TeachingType.TEACHING_PROF
        }

        self.app_user = AppUser.objects.create(**self.app_user_attributes)
        self.serializer = AppUserSerializer(instance=self.app_user)


    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'user',
            'prof_type']))

    #FIX
    def test_user_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data['user'].keys()), set([
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'is_superuser']))


    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user']['username'], self.app_user_attributes['user'].username)


    def test_prof_type_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['prof_type'], self.app_user_attributes['prof_type'])