# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-29 18:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pashinin', '0006_course_courselead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courselead',
            name='session_key',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='courselead',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
