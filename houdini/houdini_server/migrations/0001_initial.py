# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-22 08:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import houdini_server.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=32)),
                ('middle_name', models.CharField(max_length=32, null=True)),
                ('last_name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('activation_key', models.CharField(max_length=40)),
                ('key_expires', models.DateTimeField()),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', houdini_server.models.HoudiniUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('key', models.CharField(blank=True, max_length=32)),
                ('secret', models.CharField(blank=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', models.SlugField()),
                ('parents', models.ManyToManyField(blank=True, to='houdini_server.Role')),
                ('permissions', models.ManyToManyField(blank=True, to='houdini_server.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='RolesToPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.TextField()),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houdini_server.Role')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='roles',
            field=models.ManyToManyField(to='houdini_server.Role'),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(to='houdini_server.Role'),
        ),
    ]
