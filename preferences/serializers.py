from rest_framework import serializers
from rest_framework import viewsets
from django.core.exceptions import ValidationError

from users.serializers import AppUserSerializer #TODO: may not need the entire nested object: logic could handle just referencing username?
from .models import Preferences

#main Preferences serializer
class PreferencesSerializer(serializers.ModelSerializer):
    professor = serializers.CharField(required=True, source='professor.user.username')
    is_submitted = serializers.BooleanField(default=False)
    is_unavailable_sem1 = serializers.BooleanField(default=False)
    is_unavailable_sem2 = serializers.BooleanField(default=False)
    num_relief_courses = serializers.IntegerField(max_value=None, min_value=0)
    taking_sabbatical = serializers.BooleanField(default=False)
    sabbatical_length = serializers.ChoiceField(
        choices=Preferences.SabbaticalLength,
        default=Preferences.SabbaticalLength.NONE
    )
    sabbatical_start_month = serializers.IntegerField(max_value=None, min_value=0)
    preferred_hours = serializers.JSONField()
    teaching_willingness = serializers.JSONField()
    teaching_difficulty = serializers.JSONField()
    wants_topics_course = serializers.BooleanField(default=False)
    topics_course_id = serializers.CharField(max_length=20, default='')
    topics_course_name = serializers.CharField(max_length=255, default='')
    class Meta:
        model = Preferences
        fields = (
            'professor', 'is_submitted', 'is_unavailable_sem1', 'is_unavailable_sem2', 'num_relief_courses',
            'taking_sabbatical', 'sabbatical_length', 'sabbatical_start_month', 'preferred_hours',
            'teaching_willingness', 'teaching_difficulty', 'wants_topics_course', 'topics_course_id',
            'topics_course_name'
<<<<<<< HEAD
        )
=======
        )
    
>>>>>>> main
