# Generated by Django 4.0.1 on 2022-07-01 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='preferred_hours',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='teaching_difficulty',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='teaching_willingness',
            field=models.JSONField(default=dict),
        ),
    ]