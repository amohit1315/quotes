# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-15 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20181215_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='master_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.MasterCompany'),
        ),
        migrations.AddField(
            model_name='mastercompany',
            name='company_id',
            field=models.CharField(default=uuid.UUID('32992a43-2670-4130-8214-dd6f0e49fbf2'), max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='master_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.MasterCompany'),
        ),
        migrations.AddField(
            model_name='service',
            name='master_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.MasterCompany'),
        ),
        migrations.AlterField(
            model_name='mastercompany',
            name='company_name',
            field=models.CharField(max_length=255),
        ),
    ]