from django.db import models


# Create your models here.

class BaseModel(models.Model):
    """
    基础model
    """
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    def get_dict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        dict_result = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                dict_result[attr] = getattr(self, attr)
        return dict_result

    class Meta:
        abstract = True


class FlowInfo(BaseModel):
    """
    状态记录, 查看流程节点信息，展示流程图
    """
    name = models.CharField('流程名称', max_length=50)
    workflow_id = models.IntegerField('所属工作流程节点id')
    source_id = models.IntegerField('源点id')
    destination_id = models.CharField('目的状态id',  max_length=150, default='0', help_text='用于工单步骤接口时，指向的下一节点或并行的多个节点')

    modify_last_man = models.CharField('最后修改流程的人', max_length=150,)
    run_state = models.IntegerField('运行状态', default=0, help_text='0:未执行，1：正在执行，2：执行失败')
    run_info = models.CharField('运行状态信息', max_length=150, default='', help_text='正在执行、运行失败、成功')
    last_run_info = models.CharField('上一次运行状态信息', max_length=150, default='', help_text='运行失败、成功')

    def __str__(self):
        return self.name


class FlowID(BaseModel):
    """
    流程信息，查看流程图
    """
    flow_name = models.CharField('流程名称', max_length=50)
    workflow_id = models.IntegerField('流程节点id')
    flow_state = models.IntegerField('流程运行状态', default=0, help_text='0:未执行，1：正在执行，2：执行失败，3：执行完成')
    last_run_info = models.CharField('上一次运行状态信息', max_length=150, default='', help_text='运行失败、成功')

    def __str__(self):
        return self.flow_name


