# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-12 10:41
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20170512_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.Comment', verbose_name='Parent element'),
        ),
    ]
