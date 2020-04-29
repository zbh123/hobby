from django.db import models

# Create your models here.


class User(models.Model):
    office = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    login_time = models.DateTimeField('最后登录时间', auto_now=True)

    def __str__(self):
        return self.username