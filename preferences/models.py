from django.db import models

# Create your models here.
from users.models import AppUser, TeachingType
from django.utils.translation import gettext_lazy as _
from courses.models import Course



class Semester(models.TextChoices):
    SPRING = 'SPRING', _('Spring Semester')
    SUMMER = 'SUMMER', _('Summer Semester')
    FALL = 'FALL', _('Fall Semester')


class Day(models.TextChoices):
    MONDAY = 'MONDAY', _('Monday')
    TUESDAY = 'TUESDAY', _('Tuesday')
    WEDNESDAY = 'WEDNESDAY', _('Wednesday')
    THURSDAY = 'THURSDAY', _('Thursday')
    FRIDAY = 'FRIDAY', _('Friday')


class Preferences(models.Model):

    id = models.CharField(
        max_length=255,
        primary_key=True
    )

    name = models.CharField(
        max_length=255,
        primary_key=False
    )

    userData = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE
    )

    isPeng = models.BooleanField(
        default=False
    )

    """
    Dictates whether preferredNonTeachingSemester is a
    hard or soft constraint
    """
    facultyType = models.CharField(
        max_length=2,
        choices=TeachingType.choices,
        default=TeachingType.TEACHING_PROF,
    )

    coursePreferences = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    # TODO: Calculate that
    teachingObligations = models.IntegerField()

    class PreferredTime(models.Model):
        semester = models.CharField(
            max_length=6,
            choices=Semester.choices
        )
        day = models.CharField(
            max_length=9,
            choices=Day.choices
        )
        startTime = models.CharField(
            max_length=7
        )
        endTime = models.CharField(
            max_length=7
        )

    preferredTimes = models.ForeignKey(
        PreferredTime,
        on_delete=models.CASCADE
    )


# EVERYTHING BELOW THIS IS SOMETHING THAT STILL NEEDS TO BE IMPLEMENTED IN THE MODEL #
#
# preferredCoursesPerSemester: dict
# {
#     fall: int
#     spring: int
#     summer: int
# }
# Soft
# constraint.The
# number
# of
# courses
# the
# professor
# would
# like
# to
# teach in each
# semester.Must
# add
# up
# to
# the
# value
# of
# teachingObligations or the
# constraint is violated.
#
# preferredNonTeachingSemester: Semester | undefined
# An
# enum
# indicating
# the
# professor’s
# preferred
# non - teaching
# semester.If
# the
# professor is teaching
# faculty, the
# scheduler
# will
# attempt
# to
# assign
# no
# courses
# to
# them in this
# semester.It is considered
# a
# soft
# constraint
# when
# the
# facultyType is Teaching and hard
# constraint
# when
# the
# facultyType is Research.
#
# preferredCourseDaySpreads: CourseDaySpread[]
# An
# enum
# that
# indicates
# the
# instructor’s
# preferred
# allocations
# of
# lecture
# hours(e.g., Monday, Wednesday, Thursday).
