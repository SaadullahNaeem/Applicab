# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-29 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0002_auto_20170628_1916'),
        ('Booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Booking.Booking')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Driver.Driver')),
            ],
        ),
    ]