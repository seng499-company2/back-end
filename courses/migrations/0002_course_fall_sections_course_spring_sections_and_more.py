# Generated by Django 4.0.1 on 2022-07-22 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_a_coursesection_max_capacity'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='fall_sections',
            field=models.ManyToManyField(related_name='courses_fall', to='schedule.A_CourseSection'),
        ),
        migrations.AddField(
            model_name='course',
            name='spring_sections',
            field=models.ManyToManyField(related_name='courses_spring', to='schedule.A_CourseSection'),
        ),
        migrations.AddField(
            model_name='course',
            name='summer_sections',
            field=models.ManyToManyField(related_name='courses_summer', to='schedule.A_CourseSection'),
        ),
    ]
