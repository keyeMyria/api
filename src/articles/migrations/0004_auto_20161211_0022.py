# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20161208_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, default=None, editable=False, help_text='/articles/.../how-to-install-linux', max_length=765, null=True, verbose_name='In URL'),
        ),
    ]
