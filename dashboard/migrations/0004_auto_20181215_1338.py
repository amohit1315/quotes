# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-15 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_product_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBUser',
            fields=[
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('password', models.CharField(blank=True, max_length=200, null=True)),
                ('role', models.CharField(blank=True, max_length=200, null=True)),
                ('designation', models.CharField(blank=True, max_length=200, null=True)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('effective_enddate', models.DateField(blank=True, null=True)),
                ('active', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MasterCompany',
            fields=[
                ('phone_number', models.CharField(blank=True, max_length=45, null=True)),
                ('company_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('effective_enddate', models.DateField(blank=True, null=True)),
                ('active', models.CharField(blank=True, max_length=45, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='dbuser',
            name='master_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.MasterCompany'),
        ),
    ]
