from django.test import TestCase

from django.test import TestCase, RequestFactory    #**tests that interact with a database require subclassing of this class**

from django.contrib.auth.models import User
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsAdmin
from .views import CourseView, AllCoursesView

#Serializer Testing
class CourseSerializerTest(TestCase):
    @classmethod
    def setUp(self):
        #build Course and CourseSerializer instances
        self.course_attributes = {
            "course_code": "SENG499",
            "num_sections": 2,
            "course_title": "Design Project 2",
            "fall_offering": True,
            "spring_offering": True,
            "summer_offering": False,
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4
        }

        #serialize into a Course object
        self.course = Course.objects.create(**self.course_attributes)
        self.serializer = CourseSerializer(instance=self.course)


    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'course_code',
            'num_sections',
            'course_title',
            'fall_offering',
            'spring_offering',
            'summer_offering',
            'pengRequired',
            'yearRequired'
        ]))

    
    def test_valid_deserialization(self):
        serialized_data = {
            "course_code": "SENG499",
            "num_sections": 2,
            "course_title": "Design Project 2",
            "fall_offering": True,
            "spring_offering": True,
            "summer_offering": False,
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4
        }

        serializer = CourseSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

    
    def test_create_course_object(self):
        serialized_data = {
            "course_code": "SENG321",
            "num_sections": 2,
            "course_title": "Requirements Engineering",
            "fall_offering": False,
            "spring_offering": True,
            "summer_offering": False,
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4
        }

        serializer = CourseSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

       
        course_object = serializer.save()
        self.assertIsNotNone(course_object.pk)

    
    
    def test_update_course_object(self):
        #fetch course object by course_code
        course_object = Course.objects.get(course_code="SENG499")
        obj_key = course_object.pk

        #update the Course order by referencing an existing instance
        new_serialized_data = {
            "course_code": "SENG499",
            "num_sections": 2,
            "course_title": "Design Project 2 with daniella", #updated
            "fall_offering": True,
            "spring_offering": False, #updated
            "summer_offering": False,
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4
        }
        serializer = CourseSerializer(instance=course_object, data=new_serialized_data)
        self.assertTrue(serializer.is_valid())
        new_course_object = serializer.save()
        updated_obj_key = new_course_object.pk

        #assert that the same instance was updated, and updated as expected
        # self.assertEquals(updated_obj_key, obj_key)
        self.assertEquals(Course.objects.get(pk=obj_key).course_title, new_serialized_data['course_title'])
        self.assertEquals(Course.objects.get(pk=obj_key).spring_offering, new_serialized_data['spring_offering'])
    