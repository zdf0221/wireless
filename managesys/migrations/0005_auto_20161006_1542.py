# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 15:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managesys', '0004_auto_20161006_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataflow',
            old_name='Fee',
            new_name='fee',
        ),
        migrations.RenameField(
            model_name='sms',
            old_name='Fee',
            new_name='fee',
        ),
        migrations.RenameField(
            model_name='traffic',
            old_name='Fee',
            new_name='fee',
        ),
    ]
