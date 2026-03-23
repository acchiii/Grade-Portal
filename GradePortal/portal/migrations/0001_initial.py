from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('student_no', models.CharField(max_length=20, unique=True)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('email', models.EmailField(unique=True)),
                ('course', models.CharField(choices=[('BSIT','BS Information Technology'),('BSHM','BS Hospitality Management'),('BEED','BS Education (Elementary)'),('BSED','BS Education'),('BSTM','BS Tourism Management'),('BSCRIM','BS Criminology')], default='BSIT', max_length=10)),
                ('year_level', models.IntegerField(choices=[(1,'1st Year'),(2,'2nd Year'),(3,'3rd Year'),(4,'4th Year')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={'abstract': False},
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('units', models.IntegerField(default=3)),
                ('department', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True)),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('message', models.TextField()),
                ('submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('1st','1st Semester'),('2nd','2nd Semester'),('Summer','Summer')], default='1st', max_length=10)),
                ('school_yr', models.CharField(default='2026-2027', max_length=20)),
                ('prelim', models.FloatField(blank=True, null=True)),
                ('midterm', models.FloatField(blank=True, null=True)),
                ('semi', models.FloatField(blank=True, null=True)),
                ('final', models.FloatField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, choices=[('PASSED','Passed'),('FAILED','Failed'),('INC','Incomplete'),('','Pending')], default='', max_length=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='portal.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.subject')),
            ],
            options={'ordering': ['-school_yr', 'semester', 'subject__code']},
        ),
    ]
