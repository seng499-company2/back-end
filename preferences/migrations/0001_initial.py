# Generated by Django 4.0.1 on 2022-06-18 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_appuser_is_peng'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.appuser')),
                ('is_completed', models.BooleanField(default=False)),
                ('unavailable_sem1', models.CharField(max_length=7)),
                ('unavailable_sem2', models.CharField(max_length=7)),
                ('num_relief_courses', models.PositiveIntegerField()),
                ('taking_sabbatical', models.BooleanField(default=False)),
                ('sabbatical_length', models.CharField(choices=[('HALF', 'Half Length'), ('FULL', 'Full Length'), ('NONE', 'None')], default='NONE', max_length=4)),
                ('sabbatical_start_month', models.PositiveIntegerField()),
                ('preferred_hours', models.TextField()),
                ('teaching_willingness', models.TextField()),
                ('teaching_difficulty', models.TextField()),
                ('wants_topics_course', models.BooleanField(default=False)),
                ('topics_course_id', models.CharField(max_length=20)),
                ('topics_course_name', models.CharField(max_length=255)),
            ],
        ),
    ]
