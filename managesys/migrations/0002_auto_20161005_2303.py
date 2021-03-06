# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-05 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='number',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phoneNumber', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='package',
            name='dataAmount',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='localAmount',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='packFee',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='packName',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='packType',
            field=models.CharField(default='local', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='remoteAmount',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='smsAmount',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
