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
    
    # def create(self, validated_data):
    #     """
    #     Create and return a new Course instance, given the validated data.
    #     """
    #     course_json = validated_data

    #     #get the associated course object
    #     try:
    #         course_object = Course.objects.get(course_code=course_code)
    #         course = Course.objects.create(course=course_object, **validated_data)
        
    #     #raising a JSON-like exceptions
    #     except ValidationError:
    #         raise serializers.ValidationError({"error": "invalid input"})
    #     except Course.models.DoesNotExist:
    #         raise serializers.ValidationError({"error": "this course object does not exist"})
    #     return course

   
    def update(self, instance, validated_data):
        """
        Update and return an existing Preferences instance, given the validated data.
        Professor field is stored in the DB as an object; therefore the most recent AppUser object will be fetched and updated.
        """
        course_code = validated_data.pop('course_code')
        print()
        print(course_code)
        print()

        #get the most recent Professor object to update the Preferences record
        try:
            course_object = Course.objects.get(course_code=course_code)
        except Course.models.DoesNotExist:
            raise serializers.ValidationError({"error": "The associated professor object does not exist!"})

        #serialize the remaining data - professor shouldn't need to be serialized as it is an object
        instance.course = course_object
        super().update(instance, validated_data)
        return instance