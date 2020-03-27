from django.db import models

# Create your models here.


class Rpa(models.Model):
    office = models.CharField(max_length=100)
    flow_name = models.CharField(max_length=100)
    finish = models.FloatField()
    time_rpa = models.CharField(max_length=100, null=True)
    time_person = models.CharField(max_length=100, null=True)
    introduce = models.CharField(max_length=500, null=True)
    remark = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.flow_name


class IP(models.Model):
    office = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=50)

    def __str__(self):
        return self.username
