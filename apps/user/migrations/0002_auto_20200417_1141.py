# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-04-17 03:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
