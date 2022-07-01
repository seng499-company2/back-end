from django.db import models


class TimeSlot(models.Model):

    class DayOfTheWeek(models.TextChoices):
        MONDAY = 'MONDAY', _('MONDAY')
        TUESDAY = 'TUESDAY', _('TUESDAY')
        WEDNESDAY = 'WEDNESDAY', _('WEDNESDAY')
        THURSDAY = 'THURSDAY', _('THURSDAY')
        FRIDAY = 'FRIDAY', _('FRIDAY')

    '''#specifies the Many-to-One relationship with a CourseSection
    courseSection = models.ForeignKey(CourseSection, on_delete=models.CASCADE)'''
    dayOfWeek = models.CharField(
        max_length=4,
        choices=DayOfTheWeek.choices
    )
    timeRange = models.CharField(max_length=18, blank=False) #holds a single tuple of form: ("12:00","13:00")


class CourseSection(models.Model):
    professor = models.JSONField()  #{"id": AppUser.user.username, "name": AppUser.user.first_name + " " + AppUser.user.last_name}
    capacity = models.PositiveIntegerField(default=0)
    timeSlots = models.ManyToManyField(TimeSlot) #to associate multiple TimeSlot objects


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    pengRequired = models.JSONField() #{"fall": true, "spring": false, "summer": true}
    yearRequired = models.PositiveIntegerField()


class CourseOffering(models.Model):
    course = models.ManyToManyField(Course)
    sections = models.ManyToManyField(CourseSection)


class Schedule(models.Model):
    fall = models.ManyToManyField(CourseOffering)
    spring = models.ManyToManyField(CourseOffering)
    summer = models.ManyToManyField(CourseOffering)