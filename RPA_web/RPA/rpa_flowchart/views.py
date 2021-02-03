# !/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'zhubh'
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from schema import Schema, Regex, And, Or, Use, Optional
from .models import FlowInfo, FlowID
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import json
import simplejson
from collections import OrderedDict


def index(requests):
    return render(requests, 'flowchart/index.html')


class LoonBaseView(View):
    """
    base view for params validate
    """

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        request_method = request.method.lower()
        meth_schema = getattr(self, request.method.lower() + '_schema', None)
        if meth_schema and request_method in ['post', 'patch', 'put']:
            try:
                json_dict = simplejson.loads(request.body)
                meth_schema.validate(json_dict)
            except Exception as e:
                print(e.__str__())
                return HttpResponse(json.dumps(dict(code=-1, data='请求参数不合法:{}'.format(e.__str__()), msg={})),
                                    content_type="application/json")
        return handler(request, *args, **kwargs)


class WorkflowStateService(View):

    @staticmethod
    def get_workflow_states(workflow_id: int) -> tuple:
        """
        获取流程的状态列表，每个流程的state不会很多，所以不分页
        get workflow state queryset
        :param workflow_id:
        :return:
        """
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        else:
            workflow_states = FlowInfo.objects.filter(workflow_id=workflow_id, is_deleted=False).order_by('order_id')
            return True, workflow_states

    @staticmethod
    def get_workflow_states_serialize(workflow_id: int, per_page: int = 10, page: int = 1,
                                      query_value: str = '') -> tuple:
        """
        获取序列化工作流状态记录
        get restful workflow's state by params
        :param workflow_id:
        :param per_page:
        :param page:
        :param query_value:
        :return:
        """
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        query_params = Q(workflow_id=workflow_id, is_deleted=False)
        if query_value:
            query_params &= Q(name__contains=query_value)

        workflow_states = FlowInfo.objects.filter(query_params).order_by('order_id')

        paginator = Paginator(workflow_states, per_page)

        try:
            workflow_states_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_states_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            workflow_states_result_paginator = paginator.page(paginator.num_pages)
        workflow_states_object_list = workflow_states_result_paginator.object_list
        workflow_states_restful_list = []
        for workflow_states_object in workflow_states_object_list:
            flag, participant_info = WorkflowStateService.get_format_participant_info(
                workflow_states_object.participant_type_id, workflow_states_object.participant)
            result_dict = workflow_states_object.get_dict()
            result_dict['state_field_str'] = json.loads(result_dict['state_field_str'])
            result_dict['label'] = json.loads(result_dict['label'])
            result_dict['participant_info'] = participant_info

            workflow_states_restful_list.append(result_dict)
        return True, dict(workflow_states_restful_list=workflow_states_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))


class WorkflowStateView(LoonBaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is needed'),
        'workflow_id': And(int, error='workflow_id is needed'),
        'source_id': And(int, error='source_id is needed'),
        'destination_id': And(str, error='destination_id is needed'),
        'run_state': int,
        Optional('modify_last_man'): str,
        Optional('run_info'): str,
        Optional('last_run_info'): str,
        str: object
    })

    def get(self, request, *args, **kwargs):
        """
        获取工作流拥有的state列表信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        status_list = {0: 'prepare', 1: 'current', 2: 'success', 3: 'fail'}
        workflow_id = kwargs.get('workflow_id')
        request_data = request.GET
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        query_params = Q(workflow_id=workflow_id, is_deleted=False)
        workflow_states = FlowInfo.objects.filter(query_params).values()
        # print(workflow_states)
        info_list = []
        for info in workflow_states:
            # print(info)
            dest = info['destination_id'].split(',')
            for dest_id in dest:
                node = {}
                node['id'] = info['source_id']
                node['label'] = info['name'].split('\\')[-1]
                node['status'] = status_list[int(info['run_state'])]
                node['target'] = dest_id
                info_list.append(node)
        print(info_list)

        if info_list:
            code, msg, = 0, ''
        else:
            code, msg = -1, {}
        return HttpResponse(json.dumps(dict(code=code, data=info_list, msg=msg)), content_type="application/json")

    def post(self, request, *args, **kwargs):
        """
        新增状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return HttpResponse(json.dumps(dict(code=-1, data='post参数为空', msg={})), content_type="application/json")
        request_data_dict = json.loads(json_str)
        workflow_data = {}
        app_name = request.META.get('HTTP_APPNAME')
        username = request.META.get('HTTP_USERNAME')
        name = request_data_dict.get('name', '')
        is_hidden = request_data_dict.get('is_hidden', 0)
        order_id = int(request_data_dict.get('order_id', 0))
        type_id = int(request_data_dict.get('type_id', 0))
        remember_last_man_enable = int(request_data_dict.get('remember_last_man_enable', 0))
        enable_retreat = int(request_data_dict.get('enable_retreat', 0))
        participant_type_id = int(request_data_dict.get('participant_type_id', 0))

        participant = request_data_dict.get('participant', '')
        distribute_type_id = int(request_data_dict.get('distribute_type_id', 1))
        state_field_str = request_data_dict.get('state_field_str', '')
        label = request_data_dict.get('label', '')
        workflow_id = kwargs.get('workflow_id')

        flag, result = WorkflowStateService.add_workflow_state(
            workflow_id, name, is_hidden, order_id, type_id, remember_last_man_enable, participant_type_id,
            participant, distribute_type_id, state_field_str, label, username, enable_retreat)
        if flag is False:
            code, msg, data = -1, result, {}
        else:
            code, msg, data = 0, '', {'state_id': result.get('workflow_state_id')}
        return HttpResponse(json.dumps(dict(code=code, data=data, msg=msg)), content_type="application/json")


def workflow_infomation(request):
    '''
    工作流信息查询设置
    :param requests:
    :return:
    '''
    flow_dict = OrderedDict()
    query_params = Q(is_deleted=False)
    workflow_list = FlowID.objects.filter(query_params).values()
    print(len(workflow_list), workflow_list)
    for i in range(len(workflow_list)):
        id, creator, gmt_created, gmt_modified, is_deleted, flow_name, workflow_id, flow_status, last_run_info = \
        workflow_list[
            i].values()
        print(creator, gmt_created, gmt_modified, is_deleted, flow_name, workflow_id, flow_status, last_run_info)
        flow_dict[i] = {'flow_name': flow_name, 'workflow_id': workflow_id, 'flow_status': flow_status,
                        }
    head_key = ['Flow_Name', 'Workflow_ID', 'Flow_Status']
    param = {'flow_dict': flow_dict, 'head_key': head_key}
    return render(request, 'flowchart/flowinfo.html', param)


def flowchart_display(request, workflow_id):
    """
    工作流流程图
    :param request:
    :param workflow_id:
    :return:
    """
    return render(request, 'flowchart/index.html', {'workflow_id': workflow_id})
