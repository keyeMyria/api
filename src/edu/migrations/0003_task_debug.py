# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 14:10
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0002_auto_20170127_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='debug',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
