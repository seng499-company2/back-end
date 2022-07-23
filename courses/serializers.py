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
    fall_sections = A_CourseSectionSerializer(many=True, read_only=True) #nested & many-to-many
    spring_sections = A_CourseSectionSerializer(many=True, read_only=True) #nested & many-to-many
    summer_sections = A_CourseSectionSerializer(many=True, read_only=True) #nested & many-to-many

    class Meta:
        model = Course
        fields = ('course_code', 'course_title', 'pengRequired', 'yearRequired', 'fall_sections', 'spring_sections',
                  'summer_sections')
        extra_kwargs = {
            'fall_sections': {'write_only': False, 'required': False},
            'spring_sections': {'write_only': False, 'required': False},
            'summer_sections': {'write_only': False, 'required': False}
        }

    def create(self, validated_data):
        try:
            course = Course.objects.create(**validated_data)
        
        except ValidationError:
            raise serializers.ValidationError({"error": "invalid input"})
        except Course.models.DoesNotExist:
            raise serializers.ValidationError({"error": "this course object does not exist"})
        return course

   
    def update(self, instance, validated_data):

        course_code = validated_data.pop('course_code')

        try:
            course_object = Course.objects.get(course_code=course_code)
        except Course.models.DoesNotExist:
            raise serializers.ValidationError({"error": "The associated course object does not exist!"})


        instance.course = course_object
        super().update(instance, validated_data)
        return instance