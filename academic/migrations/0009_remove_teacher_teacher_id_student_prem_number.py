# Generated by Django 4.0 on 2023-10-09 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0008_student_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='teacher_id',
        ),
        migrations.AddField(
            model_name='student',
            name='prem_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
