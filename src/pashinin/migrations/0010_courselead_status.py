# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-31 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pashinin', '0009_auto_20170830_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='courselead',
            name='status',
            field=models.IntegerField(choices=[(0, 'заявка создана (не обработана)'), (1, 'отменено'), (2, 'спам'), (3, 'время подтверждено'), (4, 'я не дозвонился до клиента')], default=0, verbose_name='Статус'),
        ),
    ]
