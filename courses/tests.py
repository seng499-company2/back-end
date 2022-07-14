
from django.test import TestCase #**tests that interact with a database require subclassing of this class**

from .models import Course
from .serializers import CourseSerializer
from schedule.Schedule_models import A_Course
from schedule.adapter import get_alg_course


# Serializer Testing
class CourseSerializerTest(TestCase):
    @classmethod
    def setUp(self):
        # build Course and CourseSerializer instances
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

        # serialize into a Course object
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
        new_course_object: Course = serializer.save()
        updated_obj_key = new_course_object.pk

        #assert that the same instance was updated, and updated as expected
        # self.assertEquals(updated_obj_key, obj_key)
        self.assertEquals(Course.objects.get(pk=obj_key).course_title, new_serialized_data['course_title'])
        self.assertEquals(Course.objects.get(pk=obj_key).spring_offering, new_serialized_data['spring_offering'])

    def test_get_alg_course_create(self):
        course = self.course
        alg_course = get_alg_course(course)
        self.assertEquals(course.course_code, alg_course.code)
        self.assertEquals(course.course_title, alg_course.title)
        self.assertEquals(course.pengRequired, alg_course.pengRequired)
        self.assertEquals(course.yearRequired, alg_course.yearRequired)

    def test_get_alg_course_update(self):
        course = self.course
        alg_course = A_Course()
        alg_course.code = course.course_code
        self.assertEquals(course.course_code, alg_course.code)
        self.assertNotEquals(course.course_title, alg_course.title)
        self.assertNotEquals(course.pengRequired, alg_course.pengRequired)
        self.assertNotEquals(course.yearRequired, alg_course.yearRequired)
        alg_course = get_alg_course(course)
        self.assertEquals(course.course_code, alg_course.code)
        self.assertEquals(course.course_title, alg_course.title)
        self.assertEquals(course.pengRequired, alg_course.pengRequired)
        self.assertEquals(course.yearRequired, alg_course.yearRequired)
        try:
            alg_course2 = A_Course.objects.get(code=alg_course.code)
            self.fail()
        except A_Course.DoesNotExist:
            pass  # expected behaviour
        alg_course.save()
        alg_course2 = A_Course.objects.get(code=alg_course.code)
        self.assertEquals(course.course_code, alg_course2.code)
        self.assertEquals(course.course_title, alg_course2.title)
        self.assertEquals(course.pengRequired, alg_course2.pengRequired)
        self.assertEquals(course.yearRequired, alg_course2.yearRequired)

    def test_get_alg_course_delete(self):
        course = self.course
        alg_course = A_Course()
        alg_course.code = course.course_code
        self.assertEquals(course.course_code, alg_course.code)
        self.assertNotEquals(course.course_title, alg_course.title)
        self.assertNotEquals(course.pengRequired, alg_course.pengRequired)
        self.assertNotEquals(course.yearRequired, alg_course.yearRequired)
        alg_course = get_alg_course(course)
        alg_course.save()
        alg_course2 = A_Course.objects.get(code=alg_course.code)
        alg_course.delete()
        try:
            alg_course2 = A_Course.objects.get(code=alg_course.code)
            self.fail()
        except A_Course.DoesNotExist:
            pass  # expected behaviour

