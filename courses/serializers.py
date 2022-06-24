from rest_framework import serializers
from .models import Course
# Create your serializers here.

class CourseSerializer(serializers.Serializer):
    course_code = serializers.CharField()
    course_title = serializers.CharField()
    fall_offering = serializers.BooleanField()
    spring_offering = serializers.BooleanField()
    summer_offering = serializers.BooleanField()
    PENG_required = serializers.BooleanField()

    class Meta:
        model = Course
        fields = ('course_code', 'course_title', 'fall_offering', 'spring_offering', 'summer_offering', 'PENG_required')
