from django.db import models
from users.models import AppUser
from schedule.Schedule_models import A_CourseSection


#Front-End Base Model
class Course(models.Model):
    course_code = models.CharField(
        max_length=9,
        primary_key=True
    )
    num_sections = models.PositiveIntegerField(default=1)
    course_title = models.TextField(blank=False)
    fall_offering = models.BooleanField(default=False)
    spring_offering = models.BooleanField(default=False)
    summer_offering = models.BooleanField(default=False)
    pengRequired = models.JSONField(default=dict) #Ex: {"fall": true, "spring": false, "summer": true}
    yearRequired = models.IntegerField(default=4)
    max_capacity = models.IntegerField(default=None, null=True)
    fall_sections = models.ManyToManyField(A_CourseSection, related_name='courses_fall')
    spring_sections = models.ManyToManyField(A_CourseSection, related_name='courses_spring')
    summer_sections = models.ManyToManyField(A_CourseSection, related_name='courses_summer')

    class Meta:
        managed = True  #auto creates tables
        db_table = 'Courses'

    def __str__(self):
        return self.course_title + ' - ' + self.course_title

