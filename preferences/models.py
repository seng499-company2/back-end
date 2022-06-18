from django.db import models
from django.contrib.auth.models import User
from users.models import AppUser

from django.utils.translation import gettext_lazy as _

# Model for the database representation of a teacher Preferences record.
class Preferences(models.Model):

    class SabbaticalLength(models.TextChoices):
        HALF_LENGTH = 'HALF', _('Half Length')
        FULL_LENGTH = 'FULL', _('Full Length')
        NONE = 'NONE', _('None')

    appuser = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    is_submitted = models.BooleanField(default=False)
    unavailable_sem1 = models.CharField(max_length=7, blank=True, default='')   #'YYYY-MM'
    unavailable_sem2 = models.CharField(max_length=7, blank=True, default='')   #'YYYY-MM'
    num_relief_courses = models.PositiveIntegerField(default=0)
    taking_sabbatical = models.BooleanField(default=False)
    sabbatical_length = models.CharField(
        max_length=4,
        choices=SabbaticalLength.choices,
        default=SabbaticalLength.NONE
    )
    sabbatical_start_month = models.PositiveIntegerField(blank=True)
    preferred_hours = models.TextField(blank=True)        #holds stringified JSON object
    teaching_willingness = models.TextField(blank=True)   #holds stringified JSON object
    teaching_difficulty = models.TextField(blank=True)
    wants_topics_course = models.BooleanField(default=False)
    topics_course_id = models.CharField(max_length=20, blank=True, default='')
    topics_course_name = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        managed = True  #auto creates tables
        db_table = 'preferences'
