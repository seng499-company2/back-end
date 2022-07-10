from rest_framework import serializers
from .models import Course
from rest_framework import viewsets
from django.core.exceptions import ValidationError

import uuid

# Create your serializers here.

class CourseSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(required=True)
    num_sections = serializers.IntegerField(max_value=None, min_value=0)
    course_title = serializers.CharField()
    fall_offering = serializers.BooleanField()
    spring_offering = serializers.BooleanField()
    summer_offering = serializers.BooleanField()
    pengRequired = serializers.JSONField()
    yearRequired = serializers.IntegerField()

    class Meta:
        model = Course
        fields = ('course_code', 'num_sections', 'course_title', 'fall_offering', 'spring_offering', 'summer_offering', 'pengRequired', 'yearRequired')
    
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