# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-23 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesys', '0002_auto_20160923_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personalID',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
