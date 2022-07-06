from django.db import models
from django.contrib.postgres.fields import ArrayField
from itertools import chain
from django.utils.translation import gettext_lazy as _


class A_TimeSlot(models.Model):

    class DayOfTheWeek(models.TextChoices):
        MONDAY = 'MONDAY', _('MONDAY')
        TUESDAY = 'TUESDAY', _('TUESDAY')
        WEDNESDAY = 'WEDNESDAY', _('WEDNESDAY')
        THURSDAY = 'THURSDAY', _('THURSDAY')
        FRIDAY = 'FRIDAY', _('FRIDAY')

    dayOfWeek = models.CharField(
        max_length=9,
        choices=DayOfTheWeek.choices
    )
    timeRange = ArrayField(
        models.CharField(max_length=6, blank=False),
        size=2
    )


class A_CourseSection(models.Model):
    professor = models.JSONField()  #{"id": AppUser.user.username, "name": AppUser.user.first_name + " " + AppUser.user.last_name}
    capacity = models.PositiveIntegerField(default=0)
    timeSlots = models.ManyToManyField(A_TimeSlot, related_name='courseSections') #to associate multiple TimeSlot objects


class A_Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    pengRequired = models.JSONField() #{"fall": true, "spring": false, "summer": true}
    yearRequired = models.CharField(max_length=5)


#one instance of this class should represent a single Course & CourseSection pair
class A_CourseOffering(models.Model):
    course = models.ForeignKey(A_Course, related_name='courseOfferings', blank=True, null=True, on_delete=models.CASCADE)    #One-to-Many: course to courseOfferings
    sections = models.ManyToManyField(A_CourseSection, related_name='courseOfferings')


class A_Schedule(models.Model):
    fall = models.ManyToManyField(A_CourseOffering, related_name='fall_schedules')
    spring = models.ManyToManyField(A_CourseOffering, related_name='spring_schedules')
    summer = models.ManyToManyField(A_CourseOffering, related_name='summer_schedules')