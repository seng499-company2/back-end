from rest_framework import serializers
from rest_framework import viewsets
from django.core.exceptions import ValidationError

import users
from users.serializers import AppUserSerializer #TODO: may not need the entire nested object: logic could handle just referencing username?
from users.models import AppUser
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
        )
    
    #overrides default create
    def create(self, validated_data):
        """
        Create and return a new Preferences instance, given the validated data.
        """
        prof_username_json = validated_data.pop('professor')
        prof_username = prof_username_json['user']['username']

        #get the associated professor object (AppUser) to build a Preferences record
        try:
            prof_obj = AppUser.objects.get(user__username=prof_username)
            preferences_record = Preferences.objects.create(professor=prof_obj, **validated_data)
        
        #raising a JSON-like exceptions
        except ValidationError:
            raise serializers.ValidationError({"error": "Invalid input!"})
        except users.models.AppUser.DoesNotExist:
            raise serializers.ValidationError({"error": "The associated professor object does not exist!"})
        return preferences_record

    #overrides default update
    def update(self, instance, validated_data):
        """
        Update and return an existing Preferences instance, given the validated data.
        Professor field is stored in the DB as an object; therefore the most recent AppUser object will be fetched and updated.
        """
        prof_username_json = validated_data.pop('professor')
        prof_username = prof_username_json['user']['username']

        #get the most recent Professor object to update the Preferences record
        try:
            prof_obj = AppUser.objects.get(user__username=prof_username)
        except users.models.AppUser.DoesNotExist:
            raise serializers.ValidationError({"error": "The associated professor object does not exist!"})

        #serialize the remaining data - professor shouldn't need to be serialized as it is an object
        instance.professor = prof_obj
        super().update(instance, validated_data)
        return instance