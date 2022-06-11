from django.test import TestCase    #**tests that interact with database require subclassing of this class**
from django.contrib.auth.models import User
from .models import AppUser
from .serializers import AppUserSerializer
from .models import AppUser
from .views import ProfessorsList
from .views import Professor
from django.http import HttpRequest
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestProfessorsList(TestCase):
    @classmethod
    def setUp(self):
        # build AppUser and AppUserSerializer instances
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
        # default data for the serializer, if needed
        self.default_serializer_data = {
            'user': {
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

    def test_prof_POST(self):
        request_factory = APIRequestFactory()
        request = request_factory.post('/users/001')
        pass
    #     TODO

    def test_prof_list_GET(self):
        request_factory = APIRequestFactory()
        request = request_factory.get('/users/')
        response = ProfessorsList().get(request)
        self.assertTrue(response is not None)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        print(response.items())

