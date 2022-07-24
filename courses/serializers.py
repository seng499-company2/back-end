from rest_framework import serializers
from .models import Course
from django.core.exceptions import ValidationError
from schedule.Schedule_serializers import A_CourseSectionSerializer

import uuid

# Create your serializers here.

class CourseSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(required=True)
    course_title = serializers.CharField()
    pengRequired = serializers.JSONField()
    yearRequired = serializers.IntegerField()
    fall_sections = A_CourseSectionSerializer(many=True, read_only=False, required=False) #nested & many-to-many
    spring_sections = A_CourseSectionSerializer(many=True, read_only=False, required=False) #nested & many-to-many
    summer_sections = A_CourseSectionSerializer(many=True, read_only=False, required=False) #nested & many-to-many

    class Meta:
        model = Course
        optional_fields = ['fall_sections', 'spring_sections', 'summer_sections']
        fields = ('course_code', 'course_title', 'pengRequired', 'yearRequired', 'fall_sections', 'spring_sections', 'summer_sections')
        extra_kwargs = {
            'fall_sections': {'write_only': False, 'required': False},
            'spring_sections': {'write_only': False, 'required': False},
            'summer_sections': {'write_only': False, 'required': False}
        }

    def create(self, validated_data):
        try:
            try:
                fall_sections_data = validated_data.pop("fall_sections")
            except KeyError:
                pass  # Data is optional
            try:
                spring_sections_data = validated_data.pop('spring_sections')
            except KeyError:
                pass  # Data is optional
            try:
                summer_sections_data = validated_data.pop('summer_sections')
            except KeyError:
                pass  # Data is optional
            course = Course.objects.create(**validated_data)
            try:
                validated_data["fall_sections"] = fall_sections_data
            except UnboundLocalError:
                pass  # Data is optional
            try:
                validated_data["spring_sections"] = spring_sections_data
            except UnboundLocalError:
                pass  # Data is optional
            try:
                validated_data["summer_sections"] = summer_sections_data
            except UnboundLocalError:
                pass  # Data is optional
            self.update_sections(course, validated_data)
        
        except ValidationError:
            raise serializers.ValidationError({"error": "invalid input"})
        except Course.DoesNotExist:
            raise serializers.ValidationError({"error": "this course object does not exist"})
        return course

    def update(self, instance, validated_data):

        course_code = validated_data.pop('course_code')

        try:
            course_object = Course.objects.get(course_code=course_code)
            self.update_sections(course_object, validated_data)

        except Course.DoesNotExist:
            raise serializers.ValidationError({"error": "The associated course object does not exist!"})


        instance.course = course_object
        super().update(instance, validated_data)
        return instance

    def update_sections(self, course_object, validated_data):
        try:
            fall_sections_data = validated_data.pop('fall_sections')
            fall_sections_list = []
            for section in fall_sections_data:
                serializer = A_CourseSectionSerializer(data=section)
                if serializer.is_valid():
                    fall_sections_list.append(serializer.save())
            course_object.fall_sections.set(fall_sections_list)
        except KeyError:
            pass  # This data is optional
        try:
            spring_sections_data = validated_data.pop('spring_sections')
            spring_sections_list = []
            for section in spring_sections_data:
                serializer = A_CourseSectionSerializer(data=section)
                if serializer.is_valid():
                    spring_sections_list.append(serializer.save())
            course_object.spring_sections.set(spring_sections_list)
        except KeyError:
            pass  # This data is optional
        try:
            summer_sections_data = validated_data.pop('summer_sections')
            summer_sections_list = []
            for section in summer_sections_data:
                serializer = A_CourseSectionSerializer(data=section)
                if serializer.is_valid():
                    summer_sections_list.append(serializer.save())
            course_object.summer_sections.set(summer_sections_list)
        except KeyError:
            pass  # This data is optional