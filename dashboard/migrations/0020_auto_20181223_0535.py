# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-23 05:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_dummy_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery_notes',
            old_name='due_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='delivery_notes',
            old_name='invoice_no',
            new_name='no',
        ),
        migrations.RenameField(
            model_name='delivery_notes',
            old_name='invoice_date',
            new_name='shipping_date',
        ),
    ]
