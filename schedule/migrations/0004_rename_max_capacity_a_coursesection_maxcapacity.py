# Generated by Django 4.0.1 on 2022-07-22 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_a_coursesection_max_capacity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='a_coursesection',
            old_name='max_capacity',
            new_name='maxCapacity',
        ),
    ]