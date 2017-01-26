# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EGE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('info', models.TextField(blank=True, help_text='Сколько задач и каких? Сколько длится экзамен?', null=True)),
                ('published', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'ЕГЭ',
                'verbose_name_plural': 'ЕГЭ / ОГЭ',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=60, verbose_name='URL part')),
                ('published', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
            },
        ),
        migrations.AddField(
            model_name='ege',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ege.Subject'),
        ),
    ]