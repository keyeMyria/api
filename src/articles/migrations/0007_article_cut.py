# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20170920_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cut',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
