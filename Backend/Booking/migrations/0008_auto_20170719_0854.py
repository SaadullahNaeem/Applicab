# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-19 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0007_auto_20170718_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
