# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-04-18 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('deal', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('shop', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '商店',
                'verbose_name_plural': '商店',
            },
        ),
    ]
