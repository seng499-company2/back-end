from nis import match
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

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
    preferred_times = models.JSONField(default=dict, blank=True)
    courses_preferences = models.JSONField(default=dict, blank=True)
    preferred_non_teaching_semester = models.CharField(max_length=10,  blank=True, default='')
    preferred_courses_per_semester = models.JSONField(default=dict, blank=True)
    preferred_course_day_spreads = ArrayField(models.CharField(max_length=5, blank=False), default=list, blank=True)
    
    def __str__(self):
        return self.professor.user.first_name + ' ' + self.professor.user.last_name
    
    # Will clean up the data before adding/updating the object to the database
    def clean(self):
        if self.taking_sabbatical:
            if 'TP' == self.professor.prof_type:
                if 'FULL' == self.sabbatical_length:
                    if 1 == self.sabbatical_start_month:
                        self.preferred_courses_per_semester['spring'] = 0
                        self.preferred_courses_per_semester['summer']  = 0
                        self.preferred_times['spring'] = None
                        self.preferred_times['summer'] = None
                    elif 5 == self.sabbatical_start_month:
                        self.preferred_courses_per_semester['summer'] = 0
                        self.preferred_courses_per_semester['fall']  = 0
                        self.preferred_times['summer'] = None
                        self.preferred_times['fall'] = None
                    elif 9 == self.sabbatical_start_month:
                        self.preferred_courses_per_semester['fall'] = 0
                        self.preferred_courses_per_semester['spring']  = 0
                        self.preferred_times['fall'] = None
                        self.preferred_times['spring'] = None
                    else:
                        raise ValidationError({"Error": f'Sabbatical must start in January, May, or September. Month {self.sabbatical_start_month} invalid'})
                elif 'HALF' == self.sabbatical_length:
                    if 1 == self.sabbatical_start_month:
                        self.preferred_courses_per_semester['spring']  = 0
                        self.preferred_times['spring'] = None
                    elif 5 == self.sabbatical_start_month:
                        self.preferred_courses_per_semester['summer']  = 0
                        self.preferred_times['summer'] = None
                    elif 9 == self.sabbatical_start_month:
                        self.preferred_courses_per_semester['fall']  = 0
                        self.preferred_times['fall'] = None
                    else:
                        raise ValidationError({"Error": f'Sabbatical must start in January, May, or September. Month {self.sabbatical_start_month} invalid'})
                if self.preferred_non_teaching_semester:
                        raise ValidationError({ "Error": "Professor is on leave. No non-teaching semester allowed"})

            elif 'RP' == self.professor.prof_type:
                if 'FULL' == self.sabbatical_length:
                    self.preferred_courses_per_semester['spring'] = 0
                    self.preferred_courses_per_semester['summer']  = 0
                    self.preferred_courses_per_semester['fall']  = 0
                    self.preferred_times['spring'] = None
                    self.preferred_times['summer'] = None
                    self.preferred_times['fall'] = None
                    
                elif 'HALF' == self.sabbatical_length:
                    if 1 == self.sabbatical_start_month:
                        self.preferred_courses_per_semester['spring'] = 0
                        self.preferred_courses_per_semester['summer']  = 0
                        self.preferred_times['spring'] = None
                        self.preferred_times['summer'] = None
                    elif 7 == self.sabbatical_start_month:
                        self.preferred_courses_per_semester['summer'] = 0
                        self.preferred_courses_per_semester['fall']  = 0
                        self.preferred_times['summer'] = None
                        self.preferred_times['fall'] = None
                    else:
                        raise ValidationError({"Error": f'Sabbatical must start in January or July. Month {self.sabbatical_start_month} invalid'})
                if self.preferred_non_teaching_semester:
                        raise ValidationError({ "Error": "Professor is on leave. No non-teaching semester allowed"})

    # override save method to call clean
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        

   
    class Meta:
        managed = True  #auto creates tables
        db_table = 'preferences'
