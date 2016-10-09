# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class user(models.Model):
    personalID = models.CharField(max_length=20, primary_key=True)
    username = models.CharField(max_length=20)
    userType = models.CharField(max_length=20, default="user")
    accountNumber = models.CharField(max_length=15)


class account(models.Model):
    # username = models.ForeignKey('user', related_name="FK_username")
    personalID = models.ForeignKey('user', related_name="FK_personalID")

    accountNumber = models.CharField(max_length=15, primary_key=True)
    packNumber = models.CharField(max_length=50)
    accountFee = models.CharField(max_length=50)

    localBalance = models.IntegerField(default=0)
    remoteBalance = models.IntegerField(default=0)
    smsBalance = models.IntegerField(default=0)
    dataBalance = models.IntegerField(default=0)

    balance = models.FloatField(max_length=20)
    status = models.CharField(max_length=20)


class traffic(models.Model):
    id = models.AutoField(primary_key=True)
    callerNumber = models.CharField(max_length=20)
    receiverNumber = models.CharField(max_length=20)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    callType = models.CharField(max_length=20)
    fee = models.FloatField(max_length=20)


class sms(models.Model):
    id = models.AutoField(primary_key=True)
    senderNumber = models.CharField(max_length=20)
    receiverNumber = models.CharField(max_length=20)
    sendTime = models.DateTimeField()
    receiveTime = models.DateTimeField()
    fee = models.FloatField(max_length=20)


class dataflow(models.Model):
    id = models.AutoField(primary_key=True)
    userNumber = models.CharField(max_length=20)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    dataflow = models.CharField(max_length=20)
    fee = models.FloatField(max_length=20)


class standard(models.Model):
    id = models.AutoField(primary_key=True)
    localFee = models.CharField(max_length=20)
    smsFee = models.CharField(max_length=20)
    dataFee = models.CharField(max_length=20)
    remoteFee = models.CharField(max_length=20)


class package(models.Model):
    packNumber = models.CharField(max_length=20, primary_key=True)
    packName = models.CharField(max_length=20)
    packType = models.CharField(max_length=20)
    packFee = models.CharField(max_length=20)
    localAmount = models.CharField(max_length=20)
    smsAmount = models.CharField(max_length=20)
    dataAmount = models.CharField(max_length=20)
    remoteAmount = models.CharField(max_length=20)


class number(models.Model):
    #  当前所有可用号码
    id = models.AutoField(primary_key=True)
    phoneNumber = models.CharField(max_length=15)