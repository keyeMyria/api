# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ege', '0013_remove_task_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(help_text='Все категории, которые подходят для этой задачи в экзамене', related_name='ege_tasks', to='edu.Category', verbose_name='Tags'),
        ),
    ]