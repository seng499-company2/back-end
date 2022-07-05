from django.db import models
from itertools import chain

from django.utils.translation import gettext_lazy as _


'''A printable model class that, when superclassed, allows the child model object to be printed in Python dictionary format.'''
class PrintableModel(models.Model):
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data

    class Meta:
        abstract = True


class A_TimeSlot(PrintableModel):

    class DayOfTheWeek(models.TextChoices):
        MONDAY = 'MONDAY', _('MONDAY')
        TUESDAY = 'TUESDAY', _('TUESDAY')
        WEDNESDAY = 'WEDNESDAY', _('WEDNESDAY')
        THURSDAY = 'THURSDAY', _('THURSDAY')
        FRIDAY = 'FRIDAY', _('FRIDAY')

    '''#specifies the Many-to-One relationship with a CourseSection
    courseSection = models.ForeignKey(CourseSection, on_delete=models.CASCADE)'''
    dayOfWeek = models.CharField(
        max_length=9,
        choices=DayOfTheWeek.choices
    )
    timeRange = models.CharField(max_length=18, blank=False) #holds a single tuple of form: ("12:00","13:00")


class A_CourseSection(PrintableModel):
    professor = models.JSONField()  #{"id": AppUser.user.username, "name": AppUser.user.first_name + " " + AppUser.user.last_name}
    capacity = models.PositiveIntegerField(default=0)
    timeSlots = models.ManyToManyField(A_TimeSlot, related_name='courseSections') #to associate multiple TimeSlot objects


class A_Course(PrintableModel):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    pengRequired = models.JSONField() #{"fall": true, "spring": false, "summer": true}
    yearRequired = models.CharField(max_length=5)


#one instance of this class should represent a single Course & CourseSection pair
class A_CourseOffering(PrintableModel):
    course = models.ForeignKey(A_Course, related_name='courseOfferings', blank=True, null=True, on_delete=models.CASCADE)    #One-to-Many: course to courseOfferings
    sections = models.ManyToManyField(A_CourseSection, related_name='courseOfferings')


class A_Schedule(PrintableModel):
    fall = models.ManyToManyField(A_CourseOffering, related_name='fall_schedules')
    spring = models.ManyToManyField(A_CourseOffering, related_name='spring_schedules')
    summer = models.ManyToManyField(A_CourseOffering, related_name='summer_schedules')