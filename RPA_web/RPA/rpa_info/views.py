# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.db.models import Count
import os, json
import sys
import random
from .models import Rpa, IP
from collections import OrderedDict


# Create your views here.


def index(request):
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


def ip_display(request):
    ip_infor_dict = OrderedDict()
    ip_list = IP.objects.all().values()
    print(len(ip_list))
    for i in range(len(ip_list)):
        id, office, username, address = ip_list[i].values()
        ip_infor_dict[i] = {'id': id, 'office': office, 'username': username, 'address': address}
    head_key = ['ID', '部门', '用户名', 'IP地址']
    param = {'ip_infor_dict': ip_infor_dict, 'head_key': head_key}
    return render(request, 'ip_address.html', param)


def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


def chart(request):
    office_list = Rpa.objects.values('office').distinct()
    print(office_list, len(office_list))
    office_table = []
    for i in range(len(office_list)):
        office = str(list(office_list[i].values()))
        office = office.split("'")[1]
        print(office, type(office), '1111')
        n = Rpa.objects.filter(office=str(office)).count()
        print(n)
        # office_dict[office] = n
        if (len(office_table) == 0):
            office_table = [{'value': n, 'color': randomcolor(), 'label': office}]
        else:
            office_table.append({'value': n, 'color': randomcolor(), 'label': office})
    print(json.dumps(office_table, ensure_ascii=False))
    return render(request, 'flow_chart.html', {'office_table': json.dumps(office_table, ensure_ascii=False)})
