from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from preferences.models import Preferences

# Model for the database representation of an AppUser (attribute: django.contrib.auth.models.User).


class AppUser(models.Model):

    class TeachingType(models.TextChoices):
        TEACHING_PROF = 'TP', _('Teaching Prof')
        RESEARCH_PROF = 'RP', _('Research Prof')
        OTHER = 'OT', _('Other')


    #user: contains fields
    #   - username
    #   - password (hashed)
    #   - first_name
    #   - last_name
    #   - email
    #   - is_superuser (replaces is_admin)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    prof_type = models.CharField(
        max_length=2,
        choices=TeachingType.choices,
        default=TeachingType.TEACHING_PROF,
    )
    is_peng = models.BooleanField(default=False)
    is_form_submitted = models.BooleanField(default=False)

    class Meta:
        managed = True  #auto creates tables
        db_table = 'appuser'


    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.user.username + '@uvic.ca)'

# Use Django signals to delete User instance when AppUser is deleted. Based on: https://stackoverflow.com/a/12754229
@receiver(post_delete, sender=AppUser)
def post_delete_user(sender, instance, **kwargs):
    instance.user.delete()
    
# Use Django signals to create an associated preference when a prof AppUser is created 
@receiver(post_save, sender=AppUser)
def create_app_user_preferences(sender, instance, created, **kwargs):
    if created and instance.user.is_superuser == False:
        Preferences.objects.create(professor=instance)
    
'''#methods use Django signals to create/update AppUser instances when auth.User instances are created/updated
@receiver(post_save, sender=User)
def create_app_user(sender, instance, created, **kwargs):
    if created:
        AppUser.objects.create(user=instance)
    instance.appuser.save()

@receiver(post_save, sender=User)
def update_app_user(sender, instance, **kwargs):
    instance.appuser.save()'''