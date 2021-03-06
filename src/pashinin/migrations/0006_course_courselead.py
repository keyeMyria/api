# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-28 20:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pashinin', '0005_auto_20170405_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=60)),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('desc', models.TextField(blank=True, null=True)),
                ('results', models.TextField(blank=True, null=True)),
                ('prereq', models.TextField(blank=True, null=True)),
                ('program', models.TextField(blank=True, null=True)),
                ('time_cost', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseLead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=150)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='pashinin.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
