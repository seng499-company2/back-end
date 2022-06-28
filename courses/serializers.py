from rest_framework import serializers
from .models import Course
from rest_framework import viewsets
from django.core.exceptions import ValidationError

# Create your serializers here.

class CourseSerializer(serializers.ModelSerializer):
    course_id = serializers.CharField()
    course_code = serializers.CharField()
    course_title = serializers.CharField()
    fall_offering = serializers.BooleanField()
    spring_offering = serializers.BooleanField()
    summer_offering = serializers.BooleanField()
    PENG_required = serializers.BooleanField()

    class Meta:
        model = Course
        fields = ('course_id', 'course_code', 'course_title', 'fall_offering', 'spring_offering', 'summer_offering', 'PENG_required')
    
    def create(self, validated_data):
        try:
            course = Course.objects.create(**validated_data)
        
        except ValidationError:
            raise serializers.ValidationError({"error": "invalid input"})
        except Course.models.DoesNotExist:
            raise serializers.ValidationError({"error": "this course object does not exist"})
        return course

   
    def update(self, instance, validated_data):
        """
        Update and return an existing Preferences instance, given the validated data.
        Professor field is stored in the DB as an object; therefore the most recent AppUser object will be fetched and updated.
        """
        course_code = validated_data.pop('course_code')
        print()
        print(course_code)
        print()


        try:
            course_object = Course.objects.get(course_code=course_code)
        except Course.models.DoesNotExist:
            raise serializers.ValidationError({"error": "The associated professor object does not exist!"})


        instance.course = course_object
        super().update(instance, validated_data)
        return instance