# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Google displays first 50-60 characters of a title tag', max_length=65)),
                ('added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('text', models.TextField(verbose_name='Task')),
                ('solution', models.TextField(blank=True, null=True, verbose_name='Solution')),
                ('published', models.BooleanField(db_index=True, default=False)),
            ],
            options={
                'verbose_name_plural': 'Tasks',
                'verbose_name': 'Task',
            },
        ),
    ]
