# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-22 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_usertax_userunit'),
    ]

    operations = [
        migrations.AddField(
            model_name='tax',
            name='tax_value',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='usertax',
            name='tax_value',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
