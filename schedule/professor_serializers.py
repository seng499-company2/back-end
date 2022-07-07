from rest_framework import serializers
from .professor_models import A_CoursePreferences, A_DayTimes, A_PreferredTimes, A_Professor

class A_DayTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = A_DayTimes
        fields = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
      
class A_PreferredTimesSerializer(serializers.ModelSerializer):
    fall = A_DayTimesSerializer()
    spring = A_DayTimesSerializer()
    summer = A_DayTimesSerializer()
    class Meta:
        model = A_PreferredTimes
        fields = ['fall', 'spring', 'summer']
class A_CoursePreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = A_CoursePreferences
        fields = ['course_code', 'enthusiam_score']
    

class A_ProfessorSerializer(serializers.ModelSerializer):
    preferred_times = A_PreferredTimesSerializer()
    course_preferences = A_CoursePreferences()
    
    class Meta:
        model = A_Professor
        fields = ['id', 'name', 'isPeng', 'teaching_obligations', 'faculty_type', 'course_preferences', 'preferred_times', 'preferred_courses_per_semester', 'preferred_non_teaching_time', 'preferred_course_day_spreads']
        