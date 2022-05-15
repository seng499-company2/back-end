from django.db import models

# Create your models here.
class World(models.Model):
    """World object"""
    name = models.CharField(max_length=255)
    population = models.IntegerField()
   # display an instance of the model when necessary
    def __str__(self):
        return self.name