# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-29 02:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houdini_server', '0002_auto_20170525_0828'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='activate_url',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='application',
            name='password_set_url',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
