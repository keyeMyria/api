# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 07:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pashinin', '0004_auto_20170402_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]