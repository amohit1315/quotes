# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-23 13:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_auto_20181223_0955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotes',
            old_name='invoice_date',
            new_name='quotation_date',
        ),
        migrations.RenameField(
            model_name='quotes',
            old_name='invoice_no',
            new_name='quotation_no',
        ),
    ]