# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20171023_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True, default=None, help_text='og:description. 2–4 предложения (300 символов).', null=True),
        ),
    ]