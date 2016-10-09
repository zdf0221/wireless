# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesys', '0007_delete_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('accountNumber', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('accountType', models.CharField(max_length=50)),
                ('accountFee', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=20)),
                ('id', models.CharField(max_length=20)),
                ('balance', models.FloatField(max_length=20)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]
