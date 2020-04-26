# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Count
import os, json
import time, datetime
import sys
import random
from .models import Rpa, IP, Time, User
from collections import OrderedDict
import queue

task_queue = queue.Queue()


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
    if request.method == 'POST':
        id = int(request.POST.get('id', '-1'))
        office = request.POST.get('office')
        flow_name = request.POST.get('flow_name')
        finish = request.POST.get('finish')
        if not is_number(finish):
            finish = 0
        time_rpa = request.POST.get('time_rpa')
        time_person = request.POST.get('time_person')
        introduce = request.POST.get('introduce')
        remark = request.POST.get('remark')
        operate = request.POST.get('operate')
        print(office, flow_name, finish, time_rpa)
        if operate == 'update':
            new_param = Rpa.objects.get(id=id)
            new_param.office = office
            new_param.flow_name = flow_name
            new_param.finish = finish
            new_param.time_rpa = time_rpa
            new_param.time_person = time_person
            new_param.introduce = introduce
            new_param.remark = remark
            # new_param.done()
            new_param.save()
        elif operate == 'delete':
            Rpa.objects.get(id=id).delete()
        result = '执行成功'
        return HttpResponse({"result": json.dumps(result, ensure_ascii=False)})
    else:
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
    if request.method == 'POST':
        id = int(request.POST.get('id', '-1'))
        office = request.POST.get('office')
        username = request.POST.get('username')
        address = request.POST.get('address')
        operate = request.POST.get('operate')
        if operate == 'update':
            new_param = IP.objects.get(id=id)
            new_param.office = office
            new_param.username = username
            new_param.ip_address = address
            # new_param.done()
            new_param.save()
        elif operate == 'delete':
            IP.objects.get(id=id).delete()
        result = '执行成功'
        return HttpResponse({"result": json.dumps(result, ensure_ascii=False)})
    else:
        ip_infor_dict = OrderedDict()
        ip_list = IP.objects.all().values()
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


# def chart(request):
#     office_list = Rpa.objects.values('office').distinct()
#     print(office_list, len(office_list))
#     office_table = []
#     for i in range(len(office_list)):
#         office = str(list(office_list[i].values()))
#         office = office.split("'")[1]
#         print(office, type(office), '1111')
#         n = Rpa.objects.filter(office=str(office)).count()
#         print(n)
#         # office_dict[office] = n
#         if (len(office_table) == 0):
#             office_table = [{'value': n, 'color': randomcolor(), 'label': office}]
#         else:
#             office_table.append({'value': n, 'color': randomcolor(), 'label': office})
#     print(json.dumps(office_table, ensure_ascii=False))
#     return render(request, 'flow_chart.html', {'office_table': json.dumps(office_table, ensure_ascii=False)})


# def chart_1(request):
#     office_list = Rpa.objects.values('office').distinct()
#     print(office_list, len(office_list))
#     office_table = []
#     for i in range(len(office_list)):
#         office = str(list(office_list[i].values()))
#         office = office.split("'")[1]
#         print(office, type(office), '1111')
#         n = Rpa.objects.filter(office=str(office)).count()
#         print(n)
#         # office_dict[office] = n
#         if (len(office_table) == 0):
#             office_table = [{'label': office, 'data': n, 'color': randomcolor()}]
#         else:
#             office_table.append({'label': office, 'data': n, 'color': randomcolor()})
#     print(json.dumps(office_table, ensure_ascii=False))
#     return render(request, 'chart_1.html', {'office_table': json.dumps(office_table, ensure_ascii=False)})


def chart_2(request):
    office_list = Rpa.objects.values('office').distinct()
    # print(office_list, len(office_list))
    office_table = []
    for i in range(len(office_list)):
        office = str(list(office_list[i].values()))
        office = office.split("'")[1]
        print(office, type(office), '1111')
        n = Rpa.objects.filter(office=str(office)).count()
        # print(n)
        # office_dict[office] = n
        if (len(office_table) == 0):
            office_table = [[n, randomcolor(), office]]
        else:
            office_table.append([n, randomcolor(), office])
    # print(json.dumps(office_table, ensure_ascii=False))
    return render(request, 'chart_pie.html', {'office_table': json.dumps(office_table, ensure_ascii=False)})


# def chart_3(request):
#     flow_name_list = []
#     rpa_time = []
#     person_time = []
#     flow_list = Time.objects.all().values()
#     for i in range(len(flow_list)):
#         id, flow_name, time_rpa, time_person = flow_list[i].values()
#         if time_rpa != None and time_person != None:
#             rpa_time.append(time_rpa)
#             person_time.append(time_person)
#             flow_name_list.append(flow_name)
#     param = {'flow_name': flow_name_list, 'rpa_time': rpa_time, 'person_time': person_time}
#     print(param)
#     return render(request, 'chart_3.html', param)


def chart_4(request):
    flow_name_list = []
    rpa_time = []
    person_time = []
    ratio_list = []
    flow_list = Time.objects.all().values()
    for i in range(len(flow_list)):
        id, flow_name, time_rpa, time_person = flow_list[i].values()
        if time_rpa != None and time_person != None:
            rpa_time.append(time_rpa)
            person_time.append(time_person)
            flow_name_list.append(flow_name)
            ratio_list.append(round(float(time_rpa) / float(time_person), 2))
    office_list = Rpa.objects.values('office').distinct()
    office_table = []
    office_name = []
    for i in range(len(office_list)):
        office = str(list(office_list[i].values()))
        office = office.split("'")[1]
        n = Rpa.objects.filter(office=str(office)).count()
        # office_dict[office] = n
        office_name.append(office)
        if len(office_table) == 0:
            office_table = [{'value': n, 'name': office}]
        else:
            office_table.append({'value': n, 'name': office})
    param = {'flow_name': flow_name_list, 'rpa_time': rpa_time, 'person_time': person_time,
             'office_table': json.dumps(office_table, ensure_ascii=False),
             'ratio_list': ratio_list, 'office_name': office_name}
    # print(param)
    return render(request, 'chart_gather.html', param)


def test(request):
    if request.method == 'POST':
        id = int(request.POST.get('id', '-1'))
        office = request.POST.get('office')
        username = request.POST.get('username')
        address = request.POST.get('address')
        operate = request.POST.get('operate')
        if operate == 'update':
            new_param = IP.objects.get(id=id)
            new_param.office = office
            new_param.username = username
            new_param.ip_address = address
            # new_param.done()
            new_param.save()
        elif operate == 'delete':
            IP.objects.get(id=id).delete()
        result = '执行成功'
        return HttpResponse({"result": json.dumps(result, ensure_ascii=False)})
    else:
        ip_infor_dict = OrderedDict()
        ip_list = IP.objects.all().values()
        for i in range(len(ip_list)):
            id, office, username, address = ip_list[i].values()
            ip_infor_dict[i] = {'id': id, 'office': office, 'username': username, 'address': address}
        head_key = ['ID', '部门', '用户名', 'IP地址']
        param = {'ip_infor_dict': ip_infor_dict, 'head_key': head_key}
        return render(request, '测试.html', param)


def add_task(task_queue):
    while not task_queue.empty():
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        office, username, ip_address = task_queue.get()
        num = IP.objects.filter(office=office, username=username, ip_address=ip_address).count()
        # print(num, 1111)
        if num != 0:
            data['is_select'] = 0
        else:
            IP.objects.create(
                office=office,
                username=username,
                ip_address=ip_address
            )
            data['is_select'] = 1
        return JsonResponse(data)


def ip_edit(request):
    if request.method == 'POST':
        office = request.POST.get('office')
        username = request.POST.get('username')
        ip_address = request.POST.get('ip_address')
        # task_queue.put([office, username, ip_address])
        # print(office, username, ip_address)
        # print(task_queue.qsize())
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        num = IP.objects.filter(office=office, username=username, ip_address=ip_address).count()
        # print(num, 1111)
        # time.sleep(2)
        if num != 0:
            data['is_select'] = 0
        else:
            IP.objects.create(
                office=office,
                username=username,
                ip_address=ip_address
            )
            data['is_select'] = 1
        return JsonResponse(data)
    return render(request, 'ip_edit.html')


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def flow_edit(request):
    if request.method == 'POST':
        office = request.POST.get('office')
        flow_name = request.POST.get('flow_name')
        finish = request.POST.get('finish')
        if not is_number(finish):
            finish = 0
        time_rpa = request.POST.get('time_rpa')
        time_person = request.POST.get('time_person')
        introduce = request.POST.get('introduce')
        remark = request.POST.get('remark')
        # task_queue.put([office, username, ip_address])
        print(office, flow_name, finish, time_rpa, time_person)
        # print(task_queue.qsize())
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        num = Rpa.objects.filter(office=office, flow_name=flow_name).count()
        # print(num, 1111)
        # time.sleep(2)
        if num != 0:
            data['is_select'] = 0
        else:
            Rpa.objects.create(
                office=office,
                flow_name=flow_name,
                finish=finish,
                time_rpa=time_rpa,
                time_person=time_person,
                introduce=introduce,
                remark=remark
            )
            data['is_select'] = 1
        return JsonResponse(data)
    return render(request, 'flow_edit.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        print(username, passwd)
        num = User.objects.filter(username=username, passwd=passwd).count()
        info = User.objects.get(username=username)
        print(info)
        if num > 0:
            info = User.objects.get(username=username)
            info.login_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            info.save()
            request.session['is_login'] = 1
            request.session['username'] = username
            return redirect('/table/')
    return render(request, 'login.html')


def logout(request):
    try:
        request.session['is_login'] = 0
        del request.session['username']
    except KeyError:
        pass
    return redirect('/ip_address/')
