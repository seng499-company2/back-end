from rest_framework import serializers
from rest_framework import viewsets
from django.core.exceptions import ValidationError

from .Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering


class A_TimeSlotSerializer(serializers.ModelSerializer):
    #dayOfWeek = serializers.ChoiceField(choices=A_TimeSlot.DayOfTheWeek, required=True)
    #timeRange = serializers.CharField(required=True)
    class Meta:
        model = A_TimeSlot
        fields = ['dayOfWeek', 'timeRange'] #reverse relation courseSections removed for now


class A_CourseSectionSerializer(serializers.ModelSerializer):
    professor = serializers.JSONField()
    capacity = serializers.IntegerField(max_value=None, min_value=0)
    timeSlots = A_TimeSlotSerializer(many=True, read_only=True)     #nested & many-to-many
    class Meta:
        model = A_CourseSection
        fields = ['professor', 'capacity', 'timeSlots']


class A_CourseSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    title = serializers.CharField()
    pengRequired = serializers.JSONField() #{"fall": true, "spring": false, "summer": true}
    yearRequired = serializers.CharField()
    class Meta:
        model = A_Course
        fields = ('code', 'title', 'pengRequired', 'yearRequired') #TODO: do we need the reverse relation here?


class A_CourseOfferingSerializer(serializers.ModelSerializer):
    course = A_CourseSerializer(read_only=True)                     #nested & many-to-one
    sections = A_CourseSectionSerializer(many=True, read_only=True) #nested & many-to-many
    class Meta:
        model = A_CourseOffering
        fields = ['course', 'sections']


