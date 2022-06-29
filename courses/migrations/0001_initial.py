# Generated by Django 4.0.1 on 2022-06-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=9)),
                ('section', models.CharField(max_length=5)),
                ('course_title', models.TextField()),
                ('fall_offering', models.BooleanField()),
                ('spring_offering', models.BooleanField()),
                ('summer_offering', models.BooleanField()),
                ('PENG_required', models.BooleanField()),
            ],
            options={
                'db_table': 'Courses',
                'managed': True,
                'unique_together': {('course_code', 'section')},
            },
        ),
    ]
