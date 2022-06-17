from django.test import TestCase, RequestFactory    #**tests that interact with a database require subclassing of this class**

from django.contrib.auth.models import User
from .models import AppUser
from .serializers import AppUserSerializer
from .permissions import IsAdmin
from .views import Professor

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
            'prof_type': 'RP',
            'is_peng': True
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
            'prof_type': 'TP',
            'is_peng': True
        }

        #serialize into an AppUser object
        self.app_user = AppUser.objects.create(**self.app_user_attributes)
        self.serializer = AppUserSerializer(instance=self.app_user)


    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'user',
            'prof_type',
            'is_peng']))


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


    def test_appuser_fields_content(self):
        data = self.serializer.data
        self.assertEqual(data['prof_type'], self.app_user_attributes['prof_type'])
        self.assertEqual(data['is_peng'], self.app_user_attributes['is_peng'])

    
    def test_valid_deserialization(self):
        serialized_data = {
            'user':{
                'username': 'abcdef',
                'password': '123',
                'first_name': 'Abc',
                'last_name': 'Def',
                'email': 'abc@uvic.ca',
                'is_superuser': False
            },
            'prof_type': 'TP',
            'is_peng': True
        }
        serializer = AppUserSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

    
    def test_create_appuser_obj(self):
        serialized_data = {
            'user':{
                'username': 'abcdef',
                'password': '123',
                'first_name': 'Abc',
                'last_name': 'Def',
                'email': 'abc@uvic.ca',
                'is_superuser': False
            },
            'prof_type': 'TP',
            'is_peng': True
        }
        serializer = AppUserSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

        #use the serializer to create an AppUser record, then assert it has been committed to DB
        app_user_obj = serializer.save()
        self.assertIsNotNone(app_user_obj.pk)

    
    def test_update_appuser_obj(self):
        serialized_data = {
            'user':{
                'username': 'abcdef',
                'password': '123',
                'first_name': 'Abc',
                'last_name': 'Def',
                'email': 'abc@uvic.ca',
                'is_superuser': False
            },
            'prof_type': 'TP',
            'is_peng': True
        }
        serializer = AppUserSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

        #use the serializer to create an AppUser record
        app_user_obj = serializer.save()
        obj_key = app_user_obj.pk
        
        #now, update the AppUser record order by referencing an existing instance
        updated_serialized_data = {
            'user':{
                'username': 'ghijkl',   #updated field
                'password': '123',
                'first_name': 'Abc',
                'last_name': 'Def',
                'email': 'abc@uvic.ca',
                'is_superuser': False
            },
            'prof_type': 'RP',   #updated field
            'is_peng': True
        }
        serializer = AppUserSerializer(instance=app_user_obj, data=updated_serialized_data)
        self.assertTrue(serializer.is_valid())
        updated_app_user = serializer.save()
        updated_obj_key = updated_app_user.pk

        #assert that the same instance was updated, and updated as expected
        self.assertEquals(updated_obj_key, obj_key)
        self.assertEquals(AppUser.objects.get(pk=obj_key).user.username, updated_serialized_data['user']['username'])
        self.assertEquals(AppUser.objects.get(pk=obj_key).prof_type, updated_serialized_data['prof_type'])


    def test_updated_appuser_password_hash(self):
        serialized_data = {
            'user':{
                'username': 'abcdef',
                'password': '123',
                'first_name': 'Abc',
                'last_name': 'Def',
                'email': 'abc@uvic.ca',
                'is_superuser': False
            },
            'prof_type': 'TP',
            'is_peng': True
        }
        serializer = AppUserSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

        #use the serializer to create an AppUser record
        app_user_obj = serializer.save()
        obj_key = app_user_obj.pk
        
        #now, update the AppUser record order by referencing an existing instance
        updated_serialized_data = {
            'user':{
                'username': 'abcdef',   
                'password': 'newpass!',  #only updated field
                'first_name': 'Abc',
                'last_name': 'Def',
                'email': 'abc@uvic.ca',
                'is_superuser': False
            },
            'prof_type': 'TP',
            'is_peng': True
        }
        serializer = AppUserSerializer(instance=app_user_obj, data=updated_serialized_data)
        self.assertTrue(serializer.is_valid())
        updated_app_user = serializer.save()
        updated_obj_key = updated_app_user.pk

        #assert that the same instance was updated, and updated as expected
        self.assertEquals(updated_obj_key, obj_key)
        #check that the password is now associated and correctly hashed
        self.assertTrue(AppUser.objects.get(pk=obj_key).user.check_password('newpass!'))
        
        

class UserPermissions(TestCase):
    """ Test Permissions
        IsAdmin should return true only if user is superuser
    """
    @classmethod
    def setUp(self):
        self.admin_user = User.objects.create(username='admin', is_superuser=True, id='1')
        self.non_admin_user = User.objects.create(username='prof', is_superuser=False, id='12')
        self.factory = RequestFactory()
        self.view = Professor.as_view()

    def test_admin_user_permissions(self):
        request = self.factory.delete('/users/abcdef')
        request.user = self.admin_user
        permission_check = IsAdmin()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        obj_permissions = permission_check.has_object_permission(request, self.view, self.admin_user)
        self.assertTrue(obj_permissions)
    
    def test_non_admin_user_permissions(self):
        request = self.factory.delete('/users/abcdef')
        request.user = self.non_admin_user
        permission_check = IsAdmin()
        permission = permission_check.has_permission(request, None)
        self.assertFalse(permission)
        obj_permissions = permission_check.has_object_permission(request, self.view, self.non_admin_user)
        self.assertFalse(obj_permissions)
        
        