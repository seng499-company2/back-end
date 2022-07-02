from django.db import models

from django.utils.translation import gettext_lazy as _

# Model for the database representation of a teacher Preferences record.
class Preferences(models.Model):

    class SabbaticalLength(models.TextChoices):
        HALF_LENGTH = 'HALF', _('Half Length')
        FULL_LENGTH = 'FULL', _('Full Length')
        NONE = 'NONE', _('None')

    professor = models.OneToOneField(
        'users.AppUser',
        on_delete=models.CASCADE,
        to_field='user',
        primary_key=True
    )
    is_submitted = models.BooleanField(default=False)
    is_unavailable_sem1 = models.BooleanField(default=False)
    is_unavailable_sem2 = models.BooleanField(default=False)
    num_relief_courses = models.PositiveIntegerField(default=0)
    taking_sabbatical = models.BooleanField(default=False)
    sabbatical_length = models.CharField(
        max_length=4,
        choices=SabbaticalLength.choices,
        default=SabbaticalLength.NONE
    )
    sabbatical_start_month = models.PositiveIntegerField(default=0)
    preferred_hours = models.JSONField(default=dict)
    teaching_willingness = models.JSONField(default=dict)
    teaching_difficulty = models.JSONField(default=dict)
    wants_topics_course = models.BooleanField(default=False)
    topics_course_id = models.CharField(max_length=20, blank=True, default='')
    topics_course_name = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        managed = True  #auto creates tables
        db_table = 'preferences'
