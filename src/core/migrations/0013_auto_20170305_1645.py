# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170201_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='discord',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='skype',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]