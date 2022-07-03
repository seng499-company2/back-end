# Generated by Django 4.0.1 on 2022-07-02 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='A_Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('pengRequired', models.JSONField()),
                ('yearRequired', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='A_CourseOffering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ManyToManyField(to='schedule.A_Course')),
            ],
        ),
        migrations.CreateModel(
            name='A_TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayOfWeek', models.CharField(choices=[('MONDAY', 'MONDAY'), ('TUESDAY', 'TUESDAY'), ('WEDNESDAY', 'WEDNESDAY'), ('THURSDAY', 'THURSDAY'), ('FRIDAY', 'FRIDAY')], max_length=9)),
                ('timeRange', models.CharField(max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='A_Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fall', models.ManyToManyField(related_name='fall', to='schedule.A_CourseOffering')),
                ('spring', models.ManyToManyField(related_name='spring', to='schedule.A_CourseOffering')),
                ('summer', models.ManyToManyField(related_name='summer', to='schedule.A_CourseOffering')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='A_CourseSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professor', models.JSONField()),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('timeSlots', models.ManyToManyField(to='schedule.A_TimeSlot')),
            ],
        ),
        migrations.AddField(
            model_name='a_courseoffering',
            name='sections',
            field=models.ManyToManyField(to='schedule.A_CourseSection'),
        ),
    ]
