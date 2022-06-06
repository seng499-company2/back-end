from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    class Meta:
        managed = True  #auto creates tables
        db_table = 'appuser'

'''#methods use Django signals to create/update AppUser instances when auth.User instances are created/updated
@receiver(post_save, sender=User)
def create_app_user(sender, instance, created, **kwargs):
    if created:
        AppUser.objects.create(user=instance)
    instance.appuser.save()

@receiver(post_save, sender=User)
def update_app_user(sender, instance, **kwargs):
    instance.appuser.save()'''