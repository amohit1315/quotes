# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-21 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20181216_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('tax_category', models.CharField(max_length=500, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('unit_type', models.CharField(max_length=500, primary_key=True, serialize=False)),
            ],
        ),
    ]