# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-01 13:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='cust_followup_no',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='cust_last_contacted',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='cust_upcoming_appointment',
        ),
    ]
