# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-01 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0004_auto_20170701_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='quote',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]