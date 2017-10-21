# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pashinin', '0014_auto_20170910_0441'),
    ]

    operations = [
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('question', models.CharField(max_length=250, verbose_name='Question')),
                ('answer', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
