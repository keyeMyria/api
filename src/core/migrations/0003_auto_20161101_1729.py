# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 14:29
from __future__ import unicode_literals

import core
import dirtyfields.dirtyfields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20161030_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(blank=True, editable=False, max_length=32, null=True)),
                ('size', models.IntegerField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name_plural': 'Bin data',
                'verbose_name': 'Bin data',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('changed', models.DateTimeField(auto_now=True, db_index=True)),
                ('basename', models.CharField(blank=True, max_length=200, null=True)),
                ('sha1', models.CharField(editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('size', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('content_type', models.IntegerField(blank=True, choices=[(0, 'application'), (1, 'audio'), (2, 'example'), (3, 'image'), (4, 'message'), (5, 'model'), (6, 'multipart'), (7, 'text'), (8, 'video')], null=True)),
                ('content_subtype', models.CharField(blank=True, max_length=96, null=True)),
                ('public', models.BooleanField(default=False, help_text='Anyone can access this file')),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('uploader', models.ForeignKey(blank=True, db_column='uploader', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Files',
                'verbose_name': 'File',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='%Y/%m/%d')),
                ('date_uploaded', models.DateTimeField(default=core.now)),
                ('sha1', models.CharField(blank=True, editable=False, max_length=40, null=True, verbose_name='SHA1')),
                ('uploader', models.ForeignKey(blank=True, db_column='uploader', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Uploaded files',
                'db_table': 'uploads',
                'verbose_name': 'Uploaded file',
            },
        ),
        migrations.AlterUniqueTogether(
            name='data',
            unique_together=set([('md5', 'size')]),
        ),
        migrations.AlterIndexTogether(
            name='file',
            index_together=set([('content_type', 'content_subtype')]),
        ),
    ]
