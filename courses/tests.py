
from django.test import TestCase #**tests that interact with a database require subclassing of this class**

from .models import Course
from .serializers import CourseSerializer


# Serializer Testing
class CourseSerializerTest(TestCase):
    @classmethod
    def setUp(self):
        # build Course and CourseSerializer instances
        self.course_attributes = {
            "course_code": "SENG499",
            "course_title": "Design Project 2",
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4, 
        }

        # serialize into a Course object
        self.course = Course.objects.create(**self.course_attributes)
        self.serializer = CourseSerializer(instance=self.course)


    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'course_code',
            'course_title',
            'pengRequired',
            'yearRequired', 
            'spring_sections',
            'summer_sections',
            'fall_sections'
        ]))

    
    def test_valid_deserialization(self):
        serialized_data = {
            "course_code": "SENG499",
            "course_title": "Design Project 2",
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4,
        }

        serializer = CourseSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

    
    def test_create_course_object(self):
        serialized_data = {
            "course_code": "SENG321",
            "course_title": "Requirements Engineering",
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4,
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
            "course_title": "Design Project 2 with daniella", #updated
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4,
        }
        serializer = CourseSerializer(instance=course_object, data=new_serialized_data)
        self.assertTrue(serializer.is_valid())
        new_course_object: Course = serializer.save()
        updated_obj_key = new_course_object.pk

        #assert that the same instance was updated, and updated as expected
        self.assertEquals(Course.objects.get(pk=obj_key).course_title, new_serialized_data['course_title'])
