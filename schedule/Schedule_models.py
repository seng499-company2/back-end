from django.db import models
from django.contrib.postgres.fields import ArrayField
from itertools import chain
from django.utils.translation import gettext_lazy as _


'''PRIMARY KEY: dayOfWeek + timeRange'''
class A_TimeSlot(models.Model):

    class DayOfTheWeek(models.TextChoices):
        MONDAY = 'MONDAY', _('MONDAY')
        TUESDAY = 'TUESDAY', _('TUESDAY')
        WEDNESDAY = 'WEDNESDAY', _('WEDNESDAY')
        THURSDAY = 'THURSDAY', _('THURSDAY')
        FRIDAY = 'FRIDAY', _('FRIDAY')

    dayOfWeek = models.CharField(
        max_length=9,
        choices=DayOfTheWeek.choices,
        blank=False
    )
    timeRange = ArrayField(
        models.CharField(max_length=7, blank=False),
        size=2
    )

    #defines a primary key pair
    class Meta:
        unique_together = ('dayOfWeek', 'timeRange')

    def __str__(self):
        return str(self.dayOfWeek) + ', ' + str(self.timeRange)


'''PRIMARY KEY: id (Django auto)'''
class A_CourseSection(models.Model):
    professor = models.JSONField(null=True, blank=True)  #{"id": <int>, "name": AppUser.user.first_name + AppUser.user.last_name}
    capacity = models.PositiveIntegerField(default=0)
    timeSlots = models.ManyToManyField(A_TimeSlot, related_name='courseSections') #to associate multiple TimeSlot objects

    def __str__(self):
        related_timeSlots = [str(slot) for slot in self.timeSlots.all()]
        return 'Professor: ' + str(self.professor['name']) + ', Capacity: ' + str(self.capacity) + ', TimeSlots: ' + f'{" ".join(related_timeSlots)}'


'''PRIMARY KEY: code'''
class A_Course(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=255)
    pengRequired = models.JSONField() #{"fall": true, "spring": false, "summer": true}
    yearRequired = models.PositiveIntegerField()

    def __str__(self):
        return str(self.code)


#one instance of this class should represent a single Course & CourseSection pair
'''PRIMARY KEY: id (Django auto)'''
class A_CourseOffering(models.Model):
    course = models.ForeignKey(A_Course, related_name='courseOfferings', blank=True, null=True, on_delete=models.CASCADE)    #One-to-Many: course to courseOfferings
    sections = models.ManyToManyField(A_CourseSection, related_name='courseOfferings')

    def __str__(self):
        return 'id: ' + str(self.id) + ', ' + str(self.course.code) + ', Number of Sections: ' + str(len(self.sections.all()))


'''PRIMARY KEY: id (Django auto)'''
class A_Schedule(models.Model):
    fall = models.ManyToManyField(A_CourseOffering, related_name='fall_schedules')
    spring = models.ManyToManyField(A_CourseOffering, related_name='spring_schedules')
    summer = models.ManyToManyField(A_CourseOffering, related_name='summer_schedules')

    def __str__(self):
        return 'id: ' + str(self.id) + ', Number of Offerings: Fall: ' + str(len(self.fall.all())) + ', Spring: ' + str(len(self.spring.all())) + ', Summer: ' + str(len(self.summer.all()))