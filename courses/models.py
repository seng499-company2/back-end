from django.db import models

# Create your models here.


# JUST A STUB for testing preferences/models.py
class Course(models.Model):
    courseName = models.CharField(
        max_length=20,
    )
