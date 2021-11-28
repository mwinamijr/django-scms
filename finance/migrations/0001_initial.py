# Generated by Django 3.1.8 on 2021-11-28 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0008_teacher_short_name'),
        ('sis', '0007_auto_20210503_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('abbr', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_no', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('payer', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.IntegerField()),
                ('paid_for', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.allocation')),
                ('received_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.accountant')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sis.student')),
            ],
        ),
    ]
