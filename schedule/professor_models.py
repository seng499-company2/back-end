from django.db import models
from itertools import chain
from users.models import AppUser
from django.contrib.postgres.fields import ArrayField

from django.utils.translation import gettext_lazy as _
              

class A_DayTimes(models.Model):
    monday = ArrayField(ArrayField(
            models.CharField(max_length=7, blank=False),
            size=2))
    tuesday = ArrayField(ArrayField(
            models.CharField(max_length=7, blank=False),
            size=2))
    wednesday = ArrayField(ArrayField(
            models.CharField(max_length=7, blank=False),
            size=2))
    thursday = ArrayField(ArrayField(
            models.CharField(max_length=7, blank=False),
            size=2))
    friday = ArrayField(ArrayField(
            models.CharField(max_length=7, blank=False),
            size=2))
    saturday = ArrayField(ArrayField(
            models.CharField(max_length=7, blank=False),
            size=2))
    sunday = ArrayField(ArrayField(
            models.CharField(max_length=7, blank=False),
            size=2))
    
class A_PreferredTimes(models.Model):
    fall = models.OneToOneField(A_DayTimes)
    spring = models.OneToOneField(A_DayTimes)
    summer = models.OneToOneField(A_DayTimes)
    

class A_PreferredCoursesPerSemester(models.Model):
    fall = models.PositiveSmallIntegerField()
    spring = models.PositiveSmallIntegerField()
    summer = models.PositiveSmallIntegerField()    
    
class A_FacultyType(models.TextChoices):
        TEACHING_PROF = 'TP', _('Teaching Prof')
        RESEARCH_PROF = 'RP', _('Research Prof')
        OTHER = 'OT', _('Other')

class A_Professor(models.Model):
  id = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        to_field='user',
        primary_key=True
    )
  name = models.CharField(max_length=150)
  isPeng = models.BooleanField()
  teaching_obligations = models.PositiveSmallIntegerField()
  faculty_type = models.CharField(
        max_length=2,
        choices=A_FacultyType.choices,
        default=A_FacultyType.TEACHING_PROF,
    )
  preferred_times = models.OneToOneField(A_PreferredTimes)
  preferred_courses_per_semester = models.OneToOneField(A_PreferredCoursesPerSemester)
  preferred_non_teaching_time = models.CharField(max_length=10)
  preferred_course_day_spreads = models.CharField(max_length=10)
  
class A_CoursePreferences(models.Model):
    prof = models.ForeignKey(A_Professor)
    course_code = models.CharField(max_length=20, blank=True, default='')
    enthusiam_score = models.PositiveIntegerField(default=0)