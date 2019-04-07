# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-23 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=200)),
                ('locationx', models.FloatField()),
                ('locationy', models.FloatField()),
                ('accelerationx', models.FloatField()),
                ('accelerationy', models.FloatField()),
                ('datatime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
