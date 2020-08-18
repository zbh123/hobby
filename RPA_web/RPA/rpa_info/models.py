from django.db import models
from django.utils import timezone
import time

# Create your models here.


class Rpa(models.Model):
    office = models.CharField(max_length=100)
    flow_name = models.CharField(max_length=100)
    finish = models.FloatField()
    time_rpa = models.CharField(max_length=100, null=True)
    time_person = models.CharField(max_length=100, null=True)
    introduce = models.CharField(max_length=500, null=True)
    remark = models.CharField(max_length=500, null=True)
    start_time = models.CharField(max_length=500, null=True)
    end_time = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.flow_name


class IP(models.Model):
    office = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Time(models.Model):
    flow = models.CharField(max_length=100)
    time_rpa = models.CharField(max_length=50)
    time_person = models.CharField(max_length=50)

    def __str__(self):
        return self.flow


class User(models.Model):
    username = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    login_time = models.DateTimeField('最后登录时间', auto_now=True)

    def __str__(self):
        return self.username
