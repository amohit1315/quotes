# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-25 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_auto_20181225_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]