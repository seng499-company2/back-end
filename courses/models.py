from django.db import models

from users.models import AppUser

# Create your models here.

#Base Model

class Course(models.Model):
    course_code = models.CharField(max_length=7)
    course_title = models.TextField(blank=False)
    fall_offering = models.BooleanField()
    spring_offering = models.BooleanField()
    summer_offering = models.BooleanField()
    PENG_required = models.BooleanField()

        class Meta:
        managed = True  #auto creates tables
        db_table = 'Courses'




#Algorithm Specific Models



# class CourseSection(models.Model):
#     professor = models.OneToOneField(AppUser, primary_key = True)
#     capacity = models.IntegerField()





# class CourseOffering(models.Model):
    
    
#     course = models.ManyToManyField(
#         Course, 
#         on_delete=models.CASCADE,
#         primary_key=True
#     )

#     sections = 