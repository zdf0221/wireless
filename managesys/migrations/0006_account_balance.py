# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesys', '0005_auto_20160927_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.FloatField(default=0, max_length=10),
        ),
    ]
