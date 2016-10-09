# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-05 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesys', '0002_auto_20161005_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
        migrations.AlterField(
            model_name='account',
            name='dataBalance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='localBalance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='remoteBalance',
            field=models.IntegerField(default=0),
        ),
    ]
