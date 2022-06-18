# Generated by Django 4.0.1 on 2022-06-18 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0003_rename_user_id_preferences_appuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='num_relief_courses',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='preferred_hours',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='sabbatical_start_month',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='teaching_difficulty',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='teaching_willingness',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='topics_course_id',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='topics_course_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='unavailable_sem1',
            field=models.CharField(blank=True, default='', max_length=7),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='unavailable_sem2',
            field=models.CharField(blank=True, default='', max_length=7),
        ),
    ]
