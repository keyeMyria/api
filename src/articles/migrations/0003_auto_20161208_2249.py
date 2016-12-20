# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20161208_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, default=None, help_text='/articles/.../how-to-install-linux', max_length=765, null=True, verbose_name='In URL'),
        ),
    ]