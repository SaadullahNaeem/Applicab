# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-08 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0004_driver_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]