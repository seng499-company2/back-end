from django.test import TestCase

from django.test import TestCase, RequestFactory    #**tests that interact with a database require subclassing of this class**

from django.contrib.auth.models import User
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsAdmin
from .views import CourseView, AllCoursesView

#Serializer Testing
class AppUserSerializerTest(TestCase):
    @classmethod
    def setUp(self):
        #build AppUser and AppUserSerializer instances
        self.course_attributes = {
            "course_id": "7f57d33b-789d-47d7-b9ab-91b5c68324a7",
            "course_code": "SENG499",
            "course_title": "Design Project 2",
            "fall_offering": True,
            "spring_offering": True,
            "summer_offering": False,
            "PENG_required": True
        }

        #serialize into an AppUser object
        self.course = Course.objects.create(**self.course_attributes)
        self.serializer = CourseSerializer(instance=self.course)


    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'course_id',
            'course_code',
            'course_title',
            'fall_offering',
            'spring_offering',
            'summer_offering',
            'PENG_required']))

    
    def test_valid_deserialization(self):
        serialized_data = {
            "course_id": "7f57d33b-789d-47d7-b9ab-91b5c68324a7",
            "course_code": "SENG499",
            "course_title": "Design Project 2",
            "fall_offering": True,
            "spring_offering": True,
            "summer_offering": False,
            "PENG_required": True
        }

        serializer = CourseSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

    
    # def test_create_course_object(self):
    #     serialized_data = {
    #         "course_code": "SENG499",
    #         "course_title": "Design Project 2",
    #         "fall_offering": True,
    #         "spring_offering": True,
    #         "summer_offering": False,
    #         "PENG_required": True
    #     }

    #     serializer = CourseSerializer(data=serialized_data)
    #     self.assertTrue(serializer.is_valid())

    #     #use the serializer to create an AppUser record, then assert it has been committed to DB
    #     course_object = serializer.create(**serialized_data)
    #     self.assertIsNotNone(course_object.pk)

    

        