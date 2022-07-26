from django.test import TestCase #**tests that interact with a database require subclassing of this class**

from .models import Course
from .serializers import CourseSerializer
from schedule.Schedule_serializers import A_CourseSectionSerializer


# Serializer Testing
class CourseSerializerTest(TestCase):
    @classmethod
    def setUp(self):
        self.maxDiff = None
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

    def test_create_course_object_with_sections(self):
        serialized_data = {
            "course_code": "SENG321",
            "course_title": "Requirements Engineering",
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4,
            "fall_sections": [],
            "spring_sections": [],
            "summer_sections": [
                {
                    "professor": {"id": 0, "name": "Boss Hog"},
                    "capacity": 251,
                    "maxCapacity": 300,
                    "timeSlots": []

                }
            ]
        }

        serializer = CourseSerializer(data=serialized_data)
        self.assertTrue(serializer.is_valid())

        course_object = serializer.save()
        self.assertIsNotNone(course_object.pk)
        obj_key = course_object.pk
        # assert that the same instance was updated, and updated as expected
        self.assertEquals(Course.objects.get(pk=obj_key).course_title, serialized_data['course_title'])
        self.assertEquals(list(Course.objects.get(pk=obj_key).fall_sections.all()), serialized_data['fall_sections'])
        self.assertEquals(list(Course.objects.get(pk=obj_key).spring_sections.all()), serialized_data['spring_sections'])
        self.assertEquals(1, len(Course.objects.get(pk=obj_key).summer_sections.all()))
        summer_section = Course.objects.get(pk=obj_key).summer_sections.first()
        serializer = A_CourseSectionSerializer(instance=summer_section)
        self.assertEquals([serializer.data], serialized_data['summer_sections'])

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

    def test_update_course_section(self):
        self.maxDiff = None
        # fetch course object by course_code
        course_object = Course.objects.get(course_code="SENG499")
        obj_key = course_object.pk

        # update the Course order by referencing an existing instance
        new_serialized_data = {
            "course_code": "SENG499",
            "course_title": "This is updated",  # updated
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4,
            "fall_sections": [],
            "spring_sections": [],
            "summer_sections": [
                {
                    "professor": {"id": 0, "name": "Boss Hog"},
                    "capacity": 251,
                    "maxCapacity": 300,
                    "timeSlots": []

                }
            ]
        }
        serializer = CourseSerializer(instance=course_object, data=new_serialized_data)
        self.assertTrue(serializer.is_valid())
        new_course_object: Course = serializer.save()
        updated_obj_key = new_course_object.pk

        # assert that the same instance was updated, and updated as expected
        self.assertEquals(Course.objects.get(pk=obj_key).course_title, new_serialized_data['course_title'])
        self.assertEquals(list(Course.objects.get(pk=obj_key).fall_sections.all()), new_serialized_data['fall_sections'])
        self.assertEquals(list(Course.objects.get(pk=obj_key).spring_sections.all()), new_serialized_data['spring_sections'])
        self.assertEquals(1, len(Course.objects.get(pk=obj_key).summer_sections.all()))
        summer_section = Course.objects.get(pk=obj_key).summer_sections.first()
        serializer = A_CourseSectionSerializer(instance=summer_section)
        self.assertEquals([serializer.data], new_serialized_data['summer_sections'])



    def test_update_course_sections(self):
        self.maxDiff = None
        # fetch course object by course_code
        course_object = Course.objects.get(course_code="SENG499")
        obj_key = course_object.pk

        # update the Course order by referencing an existing instance
        new_serialized_data = {
            "course_code": "SENG499",
            "course_title": "This is updated",  # updated
            "pengRequired": {"fall": False, "spring": True, "summer": True},
            "yearRequired": 4,
            "fall_sections": [],
            "spring_sections":
            [
                {
                    "professor": {"id": 0, "name": "Boss Hog"},
                    "capacity": 251,
                    "maxCapacity": 300,
                    "timeSlots": []

                },
                {
                    "professor": {"id": 0, "name": "Big Al"},
                    "capacity": 350,
                    "maxCapacity": 500,
                    "timeSlots": []

                },
            ],
            "summer_sections": []
        }
        serializer = CourseSerializer(instance=course_object, data=new_serialized_data)
        self.assertTrue(serializer.is_valid())
        new_course_object: Course = serializer.save()
        updated_obj_key = new_course_object.pk

        # assert that the same instance was updated, and updated as expected
        self.assertEquals(Course.objects.get(pk=obj_key).course_title, new_serialized_data['course_title'])
        self.assertEquals(list(Course.objects.get(pk=obj_key).fall_sections.all()), new_serialized_data['fall_sections'])
        self.assertEquals(list(Course.objects.get(pk=obj_key).summer_sections.all()), new_serialized_data['summer_sections'])
        self.assertEquals(2, len(Course.objects.get(pk=obj_key).spring_sections.all()))
        summer_section1 = Course.objects.get(pk=obj_key).spring_sections.first()
        serializer = A_CourseSectionSerializer(instance=summer_section1)
        summer_section2 = Course.objects.get(pk=obj_key).spring_sections.all()[1]
        serializer2 = A_CourseSectionSerializer(instance=summer_section2)
        self.assertEquals([serializer.data, serializer2.data], new_serialized_data['spring_sections'])
