from django.db import models
from django.contrib.auth.models import User
from users.models import AppUser

from django.utils.translation import gettext_lazy as _

# Model for the database representation of a teacher Preference record.
class Preference(models.Model):

    class SabbaticalLength(models.TextChoices):
        HALF_LENGTH = 'HALF', _('Half Length')
        FULL_LENGTH = 'FULL', _('Full Length')
        NONE = 'NONE', _('None')

    user_id = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    is_completed = models.BooleanField(default=False)
    unavailable_sem1 = models.CharField(max_length=7)   #'YYYY-MM'
    unavailable_sem2 = models.CharField(max_length=7)   #'YYYY-MM'
    num_relief_courses = models.PositiveIntegerField()
    taking_sabbatical = models.BooleanField(default=False)
    sabbatical_length = models.CharField(
        max_length=4,
        choices=SabbaticalLength.choices,
        default=SabbaticalLength.NONE
    )
    sabbatical_start_month = models.PositiveIntegerField()
    preferred_hours = models.TextField()        #holds stringified JSON object
    teaching_willingness = models.TextField()   #holds stringified JSON object
    teaching_difficulty = models.TextField()
    wants_topics_course = models.BooleanField(default=False)
    topics_course_id = models.CharField(max_length=20)
    topics_course_name = models.CharField(max_length=255)
