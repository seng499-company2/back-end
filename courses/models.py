

from django.db import models


from users.models import AppUser

# Create your models here.

#Front-End Base Model

class Course(models.Model):
    course_code = models.CharField(max_length=9)
    section = models.CharField(max_length=5)
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
#     section_id = models.CharField(primarykeey=True, max_length=5)
#     professor = models.OneToOneField(AppUser)
#     capacity = models.IntegerField()

#     class Meta:
#         managed = True
#         db_table = "CourseSection"





# class CourseOffering(models.Model):
    
    
#     course = models.ManyToManyField(
#         Course, 
#         on_delete=models.CASCADE,
#         primary_key=True
#     )

#     sections = 