# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-25 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_auto_20181225_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit_notes',
            name='total_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]