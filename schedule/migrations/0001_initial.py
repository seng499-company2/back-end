# Generated by Django 4.0.1 on 2022-07-07 00:31

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='A_Course',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('pengRequired', models.JSONField()),
                ('yearRequired', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='A_CourseOffering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courseOfferings', to='schedule.a_course')),
            ],
        ),
        migrations.CreateModel(
            name='A_TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayOfWeek', models.CharField(choices=[('MONDAY', 'MONDAY'), ('TUESDAY', 'TUESDAY'), ('WEDNESDAY', 'WEDNESDAY'), ('THURSDAY', 'THURSDAY'), ('FRIDAY', 'FRIDAY')], max_length=9)),
                ('timeRange', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=7), size=2)),
            ],
            options={
                'unique_together': {('dayOfWeek', 'timeRange')},
            },
        ),
        migrations.CreateModel(
            name='A_Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fall', models.ManyToManyField(related_name='fall_schedules', to='schedule.A_CourseOffering')),
                ('spring', models.ManyToManyField(related_name='spring_schedules', to='schedule.A_CourseOffering')),
                ('summer', models.ManyToManyField(related_name='summer_schedules', to='schedule.A_CourseOffering')),
            ],
        ),
        migrations.CreateModel(
            name='A_CourseSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professor', models.JSONField()),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('timeSlots', models.ManyToManyField(related_name='courseSections', to='schedule.A_TimeSlot')),
            ],
        ),
        migrations.AddField(
            model_name='a_courseoffering',
            name='sections',
            field=models.ManyToManyField(related_name='courseOfferings', to='schedule.A_CourseSection'),
        ),
    ]
