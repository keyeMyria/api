# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 12:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('edu', '0007_auto_20170217_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='marked_solved_by',
            field=models.ManyToManyField(blank=True, related_name='edu_solved_tasks', to=settings.AUTH_USER_MODEL, verbose_name='People who solved'),
        ),
    ]