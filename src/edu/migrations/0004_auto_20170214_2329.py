# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 20:29
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0003_task_debug'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='solution_status',
            field=models.IntegerField(choices=[(0, 'No solution'), (1, 'Partly solved'), (2, 'Solved')], default=0, verbose_name='Solution status'),
        ),
        migrations.AlterField(
            model_name='task',
            name='debug',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]
