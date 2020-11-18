from django.db import models

# Create your models here.


class FlowStatus(models.Model):
    id = models.IntegerField('流程id', primary_key=True, unique=True, auto_created=True)
    flow_name = models.CharField('流程名', max_length=100, default='')
    flow_num = models.CharField('流程号', max_length=100, unique=True, default='')
    start_time = models.DateTimeField('创建时间', auto_now_add=True)
    result = models.CharField('执行结果', max_length=100, default='')
    machine_ip = models.CharField('机器ip', max_length=100, default='')

    def __str__(self):
        return self.flow_name


class MachineStatus(models.Model):
    id = models.IntegerField('流程id', primary_key=True, unique=True, auto_created=True)
    machine_ip = models.CharField('机器ip', max_length=100, default='')
    machine_status = models.CharField('执行状态', max_length=100, default='')

    def __str__(self):
        return self.machine_ip
