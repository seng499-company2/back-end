from django.db import models
from users.models import AppUser


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

    class Meta:
        managed = True  #auto creates tables
        db_table = 'Courses'

    def __str__(self):
        return self.course_title + ' - ' + self.course_title
    

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