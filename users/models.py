from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Model for the database representation of an AppUser (subclass of django.contrib.auth.models.User).

class AppUser(models.Model):

    class TeachingType(models.TextChoices):
        TEACHING_PROF = 'TP', _('Teaching Prof')
        RESEARCH_PROF = 'RP', _('Research Prof')
        ADMINISTRATOR = 'AD', _('Administrator')

    #id added automatically by Django - defaults to Primary Key

    #user: contains fields
    #   - username
    #   - password (hashed)
    #   - first_name
    #   - last_name
    #   - email
    #   - is_superuser (replaces is_admin)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prof_type = models.CharField(
        max_length=2,
        choices=TeachingType.choices,
        default=TeachingType.TEACHING_PROF,
    )

#methods use Django signals to create/update AppUser instances when auth.User instances are created/updated
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        AppUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

