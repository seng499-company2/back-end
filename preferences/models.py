from django.db import models

# Create your models here.


class DisplayCourse(models.Model):
    course_code = models.CharField(max_length=7)
    course_title = models.TextField(max_length=30)
    fall_offering = models.BooleanField()
    spring_offering = models.BooleanField()
    summer_offering = models.BooleanField()
    PENG_required = models.BooleanField()
