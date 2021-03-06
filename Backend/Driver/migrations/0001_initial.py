# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-28 19:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fcm_django', '0003_auto_20170313_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('language', models.CharField(max_length=30)),
                ('firebaseId', models.CharField(max_length=300)),
                ('fcmDevice', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='fcm_django.FCMDevice')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
