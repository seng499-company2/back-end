from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    taking_sabbatical = models.BooleanField(default=False)
    sabbatical_length = models.CharField(
        max_length=4,
        choices=SabbaticalLength.choices,
        default=SabbaticalLength.NONE
    )
    sabbatical_start_month = models.PositiveIntegerField(default=0)
    preferred_times = models.JSONField(default=dict)
    courses_preferences = models.JSONField(default=dict)
    preferred_non_teaching_semester = models.CharField(max_length=10,  blank=True, default='')
    preferred_courses_per_semester = models.JSONField(default=dict)
    preferred_course_day_spreads = ArrayField(models.CharField(max_length=5, blank=False), default=list)
    
    def __str__(self):
        return self.professor.first_name + ' ' + self.professor.last_name

   
    class Meta:
        managed = True  #auto creates tables
        db_table = 'preferences'
