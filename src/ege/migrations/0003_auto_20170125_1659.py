# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 13:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ege', '0002_ege_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ege',
            unique_together=set([('type', 'year', 'subject')]),
        ),
    ]
