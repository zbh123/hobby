# -*- coding:utf-8 -*-
from django.shortcuts import render
import os
import sys
from .models import Rpa
from collections import OrderedDict
# Create your views here.


def index(request):
    flow_dict = OrderedDict()
    flow_list = Rpa.objects.all().values()
    # print(len(flow_list),flow_list)
    for i in range(len(flow_list)):
        id, office, flow_name, finish, time_rpa, time_person, introduce, remark = flow_list[i].values()
        # print(id, office, flow_name, finish, time_rpa, time_person, introduce, remark)
        flow_dict[i] = {'id': id, 'office': office, 'flow_name': flow_name, 'finish': finish, 'time_rpa': time_rpa, 'time_person': time_person, 'introduce': introduce, 'remark': remark}
    head_key = ['ID', 'Office', 'Flow_name', 'Finish (%)', 'Time_rpa(m)', 'Time_person(m)', 'Introduce', 'Remark']
    param = {'flow_dict': flow_dict, 'head_key': head_key}
    return render(request, 'index.html', param)


def table(request):
    flow_dict = OrderedDict()
    flow_list = Rpa.objects.all().values()
    # print(len(flow_list),flow_list)
    for i in range(len(flow_list)):
        id, office, flow_name, finish, time_rpa, time_person, introduce, remark = flow_list[i].values()
        # print(id, office, flow_name, finish, time_rpa, time_person, introduce, remark)
        flow_dict[i] = {'id': id, 'office': office, 'flow_name': flow_name, 'finish': finish, 'time_rpa': time_rpa,
                        'time_person': time_person, 'introduce': introduce, 'remark': remark}
    head_key = ['ID', 'Office', 'Flow_name', 'Finish (%)', 'Time_rpa(m)', 'Time_person(m)', 'Introduce', 'Remark']
    param = {'flow_dict': flow_dict, 'head_key': head_key}
    return render(request, 'data_table.html', param)