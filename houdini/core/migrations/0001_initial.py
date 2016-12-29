# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 04:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlumnusProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=24)),
                ('dob', models.CharField(max_length=24)),
                ('classyear', models.IntegerField()),
                ('school', models.CharField(max_length=3)),
                ('major', models.CharField(max_length=128)),
                ('race', models.CharField(max_length=64)),
                ('sex', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicantProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classyear', models.IntegerField()),
                ('school', models.CharField(max_length=3)),
                ('major', models.CharField(max_length=128)),
                ('race', models.CharField(max_length=64)),
                ('sex', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('app_key', models.CharField(max_length=32)),
                ('app_secret', models.CharField(max_length=32)),
                ('profiles', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=24)),
                ('dob', models.CharField(max_length=24)),
                ('classyear', models.IntegerField()),
                ('school', models.CharField(max_length=3)),
                ('major', models.CharField(max_length=128)),
                ('race', models.CharField(max_length=64)),
                ('sex', models.CharField(max_length=32)),
                ('is_abroad', models.BooleanField(default=False)),
                ('home_service', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', models.SlugField()),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Role')),
                ('permissions', models.ManyToManyField(to='core.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=32)),
                ('middle_name', models.CharField(max_length=32, null=True)),
                ('last_name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=32, unique=True)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('address1', models.CharField(max_length=128, null=True)),
                ('address2', models.CharField(max_length=128, null=True)),
                ('city', models.CharField(max_length=128, null=True)),
                ('state', models.CharField(max_length=64, null=True)),
                ('zip', models.CharField(max_length=11, null=True)),
                ('roles', models.ManyToManyField(to='core.Role')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.User'),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.User'),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.User'),
        ),
        migrations.AddField(
            model_name='alumnusprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.User'),
        ),
    ]
