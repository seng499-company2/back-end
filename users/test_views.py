from django.test import TestCase  # **tests that interact with database require subclassing of this class**
from django.contrib.auth.models import User
from .serializers import AppUserSerializer
from .models import AppUser
from .views import ProfessorsList
from .views import Professor
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import SlidingToken


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
            'prof_type': AppUser.TeachingType.TEACHING_PROF,
            'is_peng': False,
            'is_form_submitted': False,
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
            'prof_type': AppUser.TeachingType.TEACHING_PROF,
            'is_peng': False,
            'is_form_submitted': False,
        }
        
        # Admin user data for the serializer, if needed
        self.admin_serializer_data = {
            'user': {
                'username': 'ece_admin',
                'password': 'ieee',
                'first_name': 'ecee',
                'last_name': 'Elc',
                'email': 'ecet@uvic.ca',
                'is_superuser': True
            },
            'prof_type': AppUser.TeachingType.OTHER,
            'is_peng': False,
            'is_form_submitted': False,
        }

        self.app_user = AppUser.objects.create(**self.app_user_attributes)
        self.serializer = AppUserSerializer(instance=self.app_user)

    @classmethod
    def save_default_user(self):
        serializer = AppUserSerializer(data=self.default_serializer_data)
        if serializer.is_valid():
            serializer.save()
            
    @classmethod
    def save_admin_user(self):
        serializer = AppUserSerializer(data=self.admin_serializer_data)
        if serializer.is_valid():
            serializer.save()

    def test_prof_update_POST(self):
        self.save_default_user()
        request_factory = APIRequestFactory()
        request = request_factory.post('/users/abcdef', data=self.default_serializer_data, format='json')
        request.user = User.objects.create_user("admin", is_superuser=True)
        response = Professor().post(request, professor_id='abcdef')
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_prof_creation_POST(self):
        request_factory = APIRequestFactory()
        request = request_factory.post('/users/', data=self.default_serializer_data, format='json')
        request.user = User.objects.create_user("admin", is_superuser=True)
        response = ProfessorsList().post(request)
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_prof_list_GET(self):
        self.save_default_user()
        self.save_admin_user()
        request_factory = APIRequestFactory()
        request = request_factory.get('/users/')
        request.user = User.objects.create_user("admin", is_superuser=True)
        response: HttpResponse = ProfessorsList().get(request)
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.maxDiff = None
        self.assertContains(response, "\"user\": {\"username\": \"johnd1\"")
        self.assertContains(response, "\"user\": {\"username\": \"abcdef\"")
        self.assertNotContains(response, "\"user\": {\"username\": \"ece_admin\"")

    def test_prof_DELETE(self):
        request_factory = APIRequestFactory()
        request = request_factory.delete('/users/abcdef')
        request.user = User.objects.create_user("admin", is_superuser=True)
        self.save_default_user()
        response = Professor().delete(request, professor_id='abcdef')
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_prof_DELETE__not_found(self):
        request_factory = APIRequestFactory()
        request = request_factory.delete('/users/doesNotExist')
        self.save_default_user()
        request.user = User.objects.create_user("admin", is_superuser=True)
        response = Professor().delete(request, professor_id='doesNotExist')
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        
    def test_prof_DELETE__check_users(self):
        self.save_default_user()
        client = APIClient()
        user = User.objects.create_user("admin", is_superuser=True)
        deleted_user = User.objects.filter(username='abcdef').get()
        self.assertEqual(3, User.objects.count())
        self.assertTrue(User.objects.contains(deleted_user))
        token = SlidingToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.delete('/api/users/abcdef/', format='json')
        self.assertIsNotNone(response)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(User.objects.contains(deleted_user))
        self.assertEqual(2, User.objects.count())
        
    def test_user_GET(self):
        self.save_default_user()
        client = APIClient()
        token = SlidingToken.for_user(self.user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get('/api/user/', format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "\"user\": {\"username\": \"johnd1\"")
    
    def test_user_GET__not_found(self):
        non_registered_user = User.objects.create_user(username='nope', email='nope@test.com', password='nope', is_superuser=False)
        client = APIClient()
        token = SlidingToken.for_user(non_registered_user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get('/api/user/', format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)     
        
    def test_user_GET__missing_token(self):
        client = APIClient()
        response = client.get('/api/user/', format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    
    
    """
    Test View Permissions
    """
    def test_admin_superuser_view_access(self):
        self.save_default_user()
        user = User.objects.create_user(username='admin', email='admin@test.com', password='admin', is_superuser=True)
        client = APIClient()
        token = SlidingToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get('/api/users/', format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "\"user\": {\"username\": \"johnd1\"")
        self.assertContains(response, "\"user\": {\"username\": \"abcdef\"")
    
    def test_get_admin_errors_not_superuser(self):
        user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
        client = APIClient()
        token = SlidingToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get('/api/users/', format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_auth_errors_not_bearer_token(self):
        user = User.objects.create_user(username='non-admin', email='noadmin@test.com', password='nope', is_superuser=False)
        client = APIClient()
        token = SlidingToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = client.get('/api/users/', format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_auth_errors_no_user(self):
        client = APIClient()
        response = client.get('/api/users/', format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTokenLogin(TestCase):
    @classmethod
    def setUp(self):
        self.client = APIClient()
        
    def test_login_token_superuser(self):
        User.objects.create_user(username='admin', email='admin@test.com', password='admin', is_superuser=True)
        response = self.client.post('/api/login/', {'username':'admin', 'password':'admin'}, format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
    
    def test_login_token_non_superuser(self):
        User.objects.create_user(username='nonadmin', email='nonadmin@test.com', password='nonadmin', is_superuser=False)
        response = self.client.post('/api/login/', {'username':'nonadmin', 'password':'nonadmin'}, format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
    
    def test_get_auth_errors_invalid_password(self):
        User.objects.create_user(username='admin', email='admin@test.com', password='admin', is_superuser=True)
        response = self.client.post('/api/login/', {'username':'admin', 'password':'pass'}, format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('token' in response.data)
    
    def test_get_auth_errors_invalid_data(self):
        User.objects.create_user(username='admin', email='admin@test.com', password='admin', is_superuser=True)
        response = self.client.post('/api/login/', {'usernameee':'admin', 'password':'admin'}, format='json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse('token' in response.data)