# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-30 00:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20161229_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='parents',
            field=models.ManyToManyField(blank=True, related_name='_role_parents_+', to='core.Role'),
        ),
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='core.Permission'),
        ),
    ]
