from django.test import TestCase  # **tests that interact with database require subclassing of this class**
from django.contrib.auth.models import User
from .serializers import AppUserSerializer
from .models import AppUser
from .views import ProfessorsList
from .views import Professor
from rest_framework import status
from rest_framework.test import APIRequestFactory
from django.http import HttpResponse


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

    @classmethod
    def save_default_user(self):
        serializer = AppUserSerializer(data=self.default_serializer_data)
        if serializer.is_valid():
            serializer.save()

    def test_prof_update_POST(self):
        self.save_default_user()
        request_factory = APIRequestFactory()
        request = request_factory.post('/users/abcdef', data=self.default_serializer_data, format='json')
        response = Professor().post(request, requested_pk='abcdef')
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_prof_createion_POST(self):
        request_factory = APIRequestFactory()
        request = request_factory.post('/users/', data=self.default_serializer_data, format='json')
        response = ProfessorsList().post(request)
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_prof_list_GET(self):
        self.save_default_user()
        request_factory = APIRequestFactory()
        request = request_factory.get('/users/')
        response: HttpResponse = ProfessorsList().get(request)
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.maxDiff = None
        self.assertContains(response, "\"user\": {\"username\": \"johnd1\"")
        self.assertContains(response, "\"user\": {\"username\": \"abcdef\"")

    def test_prof_DELETE(self):
        self.save_default_user()
        request_factory = APIRequestFactory()
        request = request_factory.delete('/users/abcdef')
        response = Professor().delete(request, requested_pk='abcdef')
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
