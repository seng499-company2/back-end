# Generated by Django 4.0.1 on 2022-07-20 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_alter_a_coursesection_professor'),
    ]

    operations = [
        migrations.AddField(
            model_name='a_coursesection',
            name='max_capacity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
