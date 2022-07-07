from rest_framework import serializers
from .Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering


class A_TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = A_TimeSlot
        fields = ['dayOfWeek', 'timeRange']

class A_CourseSectionSerializer(serializers.ModelSerializer):
    professor = serializers.JSONField() #Ex: #{"id": mzastre, "name": Mike Zastre}
    capacity = serializers.IntegerField(max_value=None, min_value=0)
    timeSlots = A_TimeSlotSerializer(many=True, read_only=True)     #nested & many-to-many
    class Meta:
        model = A_CourseSection
        fields = ['professor', 'capacity', 'timeSlots']


class A_CourseSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    title = serializers.CharField()
    pengRequired = serializers.JSONField() #Ex: {"fall": true, "spring": false, "summer": true}
    yearRequired = serializers.IntegerField(min_value=0)
    class Meta:
        model = A_Course
        fields = ('code', 'title', 'pengRequired', 'yearRequired')


class A_CourseOfferingSerializer(serializers.ModelSerializer):
    course = A_CourseSerializer(read_only=True)                     #nested & many-to-one
    sections = A_CourseSectionSerializer(many=True, read_only=True) #nested & many-to-many
    class Meta:
        model = A_CourseOffering
        fields = ['course', 'sections']


class A_ScheduleSerializer(serializers.ModelSerializer):
    fall = A_CourseOfferingSerializer(many=True, read_only = True)
    spring = A_CourseOfferingSerializer(many=True, read_only = True)
    summer = A_CourseOfferingSerializer(many=True, read_only = True)
    class Meta:
        model = A_Schedule
        fields = ['fall', 'spring', 'summer']


