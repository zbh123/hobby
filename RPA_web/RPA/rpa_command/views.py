# !/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'zhubh'
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.http import JsonResponse
import datetime
from urllib import request
import json
import os, sys
from .models import FlowStatus, MachineStatus
import requests
import logging
import time

# 一部接口
api_flow = 'http://10.32.132.27/vesta/vesta_rpa?method=callback'


basedir = os.path.dirname(__file__)
logpath = os.path.join(basedir, 'log')
if not os.path.exists(logpath):
    os.mkdir(logpath)
logname = '%s_log.txt' % time.strftime("%Y-%m-%d", time.localtime(time.time()))
logfile = os.path.join(logpath, logname)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename=logfile, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


class BaseInfo(View):
    def __init__(self):
        self.AomFile = r'C:\Users\Administrator\Desktop\Agent\Temp\AomScript.py'
        # self.FsServerIP = '10.32.90.187'
        self.FsServerIP = '10.29.132.76'
        self.FsPort = '12580'
        self.REQUEST_URL = "http://%s:%s/CallFunc.aom" % (self.FsServerIP, self.FsPort)  # 请求地址
        self.IDD_Return = "{50043442-8A69-4A6B-A8B5-61F882EDE4F3}"  # 返回消息
        self.IDD_DMName = "{9F8E5ECB-5976-4315-B8F3-43B8502B694D}"  # 类文件
        self.IDD_lpName = "{2881E26D-62CE-4937-B4BB-8998440417C4}"  # 方法
        self.IDD_GlobalID = "{9D81EE66-3CD3-428B-BB3A-F67111F70CAE}"  # GlobalID
        self.IDD_Message = "{BBA7501B-B7A9-492A-96EC-4E44C310832C}"  # 消息


    # def getToken(self):
    #     '''获取token'''
    #     with open(self.AomFile, 'r') as fp:
    #         content = fp.readlines()
    #     for line in content:
    #         if line.startswith('FsRemoteID = '):
    #             print(line.split('FsRemoteID = ')[-1].strip())
    #             FsRemoteID = line.split('FsRemoteID = ')[-1].strip().replace('"', '')
    #             return FsRemoteID
    #     return False
    def getToken(self):
        '''获取token'''

        try:
            request_body = [{"Value": "TBaseDM", "Type": 4, "Name": "{9F8E5ECB-5976-4315-B8F3-43B8502B694D}"},
                            {"Value": "admin", "Type": 4, "Name": "User"},
                            {"Value": "6FCF122292F9AD338CE66917A4247D18", "Type": 4, "Name": "Pass"},
                            {"Value": "Test1", "Type": 4, "Name": "{2881E26D-62CE-4937-B4BB-8998440417C4}"}]
            print(request_body)
            resp_data = self.CallFunc(request_body)
            print(resp_data)
            token = self.parse_json(resp_data, 'Token')
            print(token)
            result = self.parse_json(resp_data, self.IDD_Return)
            print(result)
            if result != '':
                logging.debug('调用获取Token组件失败，失败信息：', result)
                print('调用获取Token组件失败，失败信息：', result)
            else:
                return token
        except Exception as e:
            logging.debug('调用Test1函数获取Token失败，失败信息：', e)
            print('调用Test1函数获取Token失败，失败信息：', e)
            return False

    def CallFunc(self, body):
        '''请求后台'''
        try:
            if self.REQUEST_URL == "":
                return "Path cannot be empty"

            req = request.Request(self.REQUEST_URL, data=json.dumps(body).encode('gbk'))
            f = request.urlopen(req)
            try:
                return f.read()
            finally:
                f.close()
        except Exception as e:
            return str(e)

    def parse_json(self, json_data, value_name="Value"):
        '''解析json返回值'''
        try:
            for jdata in json.loads(json_data, strict=False):
                if jdata["Name"] == self.IDD_Return:
                    return jdata["Value"]
                if jdata["Name"] == value_name:
                    return jdata["Value"]
            return json.loads(json_data, strict=False)
        except Exception as e:
            return str(e)


class StartFlow(BaseInfo):

    def save_param(self):
        # 查询到的数据是二进制
        json_bytes = self.request.body
        print(json_bytes)
        # 需要进行解码，转成字符串
        json_str = json_bytes.decode('utf-8')
        print(json_str)
        # 在把字符串转换成json字典
        data = json.loads(json_str)
        FlowName = data.get('FlowName', '')
        FlowNum = str(data.get('FlowNum', ''))
        flag = str(data.get('flag', '0')).strip()
        print(FlowName, FlowNum, flag)
        if 'TA' in FlowName:
            ip = '10.0.0.157'
        elif 'FA' in FlowName:
            ip = '10.0.0.158'
        else:
            ip = '10.0.0.2'

        logging.info('StartFlow  save_param: FlowName is %s, FlowNum is %s, flag is: %s' % (FlowName, FlowNum, flag))
        if flag != '0':
            logging.info(
                'StartFlow  save_param: FlowNum %s 流程二次或多次开启' % FlowNum)
            result = FlowStatus.objects.filter(flow_num=FlowNum)
            if not result.exists():
                FlowStatus.objects.create(
                    flow_name=FlowName,
                    flow_num=FlowNum,
                    machine_ip=ip,
                    result='正在执行'
                )
                logging.info(
                    'StartFlow  save_param: FlowNum %s 已重新创建' % FlowNum)
            return 'True'


        # 根据机器IP获取机器状态
        machine_status = MachineStatus.objects.filter(machine_ip=ip).values()
        print(machine_status)
        if machine_status[0]['machine_status'] != '0':
            logging.warning('StartFlow  save_param: ip: %s 资源繁忙' % ip)
            return '资源繁忙'
        try:
            FlowStatus.objects.create(
                flow_name=FlowName,
                flow_num=FlowNum,
                machine_ip=ip,
                result='正在执行'
            )
        except:
            logging.warning('StartFlow  save_param: FlowNum %s 流程号已存在' % FlowNum)
            return '流程号已存在'
        new_param = MachineStatus.objects.get(machine_ip=ip)
        new_param.machine_status = 1
        new_param.save()
        return 'True'

    def post(self, *args):
        '''执行流程'''
        result_save = self.save_param()
        if result_save != 'True':
            result = {'result': result_save}
            return HttpResponse(json.dumps(result))
        # sName = r'测试\录屏测试'
        # 查询到的数据是二进制
        json_bytes = self.request.body
        print(json_bytes)
        # 需要进行解码，转成字符串
        json_str = json_bytes.decode('utf-8')
        print(json_str)
        # 在把字符串转换成json字典
        data = json.loads(json_str)
        FlowName = data.get('FlowName', '')
        print(FlowName)
        try:
            request_body = [{"Value": "TFlowDM", "Type": 4, "Name": self.IDD_DMName},
                            {"Value": 'zhubh', "Type": 4, "Name": "AppName"},
                            {"Value": '2B710FC391E9413CAFFA048E91120257', "Type": 4, "Name": "AppPass"},
                            # {"Value": self.getToken(), "Type": 4, "Name": "Token"},
                            {"Value": "ScriptStartFlow", "Type": 4, "Name": self.IDD_lpName},
                            {"Value": FlowName, "Type": 4, "Name": "FlowPath"}
                            ]
            print(request_body)
            resp_data = self.CallFunc(request_body)
            # print(resp_data)
            result = self.parse_json(resp_data, self.IDD_Return)
            print(result)
            if result == '':
                logging.info('StartFlow post: FlowName : %s 流程执行成功' % FlowName)
            else:
                # 这一步的流程失败可能是流程名不存在，所以需要回复状态
                if 'TA' in FlowName:
                    ip = '10.0.0.157'
                elif 'FA' in FlowName:
                    ip = '10.0.0.158'
                machine_status = MachineStatus.objects.filter(machine_ip=ip)[0]
                machine_status.machine_status = 0
                machine_status.save()
                logging.warning('StartFlow post: FlowName : %s 流程执行失败，失败信息：%s' % (FlowName, result))

        except Exception as e:
            logging.warning('StartFlow post: FlowName : %s 流程名称不正确' % FlowName)
            result = {'result': '流程名称不正确'}
            return HttpResponse(json.dumps(result))

        return JsonResponse({
            'FlowName': FlowName,
            'result': result,
        }, status=201)

    def get(self, *args):
        '''执行流程'''
        FlowName = self.request.GET.get('FlowName', '')
        print(FlowName)
        request_body = [{"Value": "TFlowDM", "Type": 4, "Name": self.IDD_DMName},
                        {"Value": self.getToken(), "Type": 4, "Name": "Token"},
                        {"Value": "ScriptStartFlow", "Type": 4, "Name": self.IDD_lpName},
                        {"Value": FlowName, "Type": 4, "Name": "FlowPath"}
                        ]
        # print(request_body)
        resp_data = self.CallFunc(request_body)
        # print(resp_data)
        print(self.parse_json(resp_data, self.IDD_Return))
        return HttpResponse('成功')


class Machine_Status(View):
    '''
        获取机器状态
    '''

    def post(self, *args):
        # 查询到的数据是二进制
        json_bytes = self.request.body
        # print(json_bytes)
        # 需要进行解码，转成字符串
        json_str = json_bytes.decode('utf-8')
        print(json_str)
        # 在把字符串转换成json字典
        data = json.loads(json_str)
        # 获取流程号
        FlowNum = str(data.get('FlowNum', ''))
        # 根据流程号获取机器ip
        ip = FlowStatus.objects.filter(flow_num=FlowNum).values()
        # print(ip)
        # print(ip[0])
        # 根据机器IP获取机器状态
        machine_status = MachineStatus.objects.filter(machine_ip=ip[0]['machine_ip']).values()
        result = {'FlowNum': FlowNum, 'result': machine_status[0]['machine_status']}
        logging.info('Machine_Status post: 流程号：%s, 机器状态：%s' % (FlowNum, machine_status[0]['machine_status']))
        return HttpResponse(json.dumps(result))


class FlowResult(View):
    '''
    设置流程状态，以及机器状态，即流程结果调用该接口，并将结果反馈给一部
    '''

    def post(self, *args):
        # 查询到的数据是二进制
        json_bytes = self.request.body
        # print(json_bytes)
        # 需要进行解码，转成字符串
        json_str = json_bytes.decode('utf-8')
        print(json_str)
        # 在把字符串转换成json字典
        data = json.loads(json_str.replace('\\', '\\\\'))
        # 获取流程名和流程结果
        FlowName = str(data.get('FlowName', ''))
        flow_result = str(data.get('FlowResult', ''))
        logging.info('FlowResult post: 流程名：%s, 流程执行结果：%s' % (FlowName, flow_result))
        # 将流程结果保存到FlowStatus中
        try:
            flow = FlowStatus.objects.filter(flow_name=FlowName).order_by('-id')[0]
            flow.result = flow_result
            flow.save()
        except Exception as e:
            print(e)
            result = {'FlowName': FlowName, 'result': '流程名不存在'}
            logging.warning('FlowResult post: 查询流程状态失败，流程名%s不存在' % flow_result)
            return HttpResponse(json.dumps(result))

        # 根据流程名查找机器IP
        flow_num = FlowStatus.objects.filter(flow_name=FlowName).order_by('-id').values()
        # print(flow_num)
        # 根据机器IP修改MachineStatus的状态
        machine_status = MachineStatus.objects.filter(machine_ip=flow_num[0]['machine_ip'])[0]
        machine_status.machine_status = 0
        machine_status.save()
        if flow_result == '成功' or flow_result == 'True':
            resultCode = '0000'
            logging.info('FlowResult post: 流程名:%s, 流程执行成功' % FlowName)
        else:
            resultCode = '1000'
            logging.info('FlowResult post: 流程名:%s, 流程执行失败，失败信息：%s' % (FlowName, flow_result))
        resultMsg = flow_result

        data = {"FlowNum": flow_num[0]['flow_num'], "FlowName": flow_num[0]['flow_name'], "resultCode": resultCode,
                "resultMsg": resultMsg}
        try:
            response = requests.post(api_flow, data=json.dumps(data))
        except Exception as e:
            logging.debug('FlowResult post: 回调API失败，失败信息：%s' % e)
            print('回调函数报错，错误内容：', e)
        # data = response.json()
        # print(data)
        result = {'FlowName': FlowName, 'result': '成功'}
        return HttpResponse(json.dumps(result))


class StopFlow(BaseInfo):

    def post(self, *args):
        '''执行流程'''
        # sName = r'测试\录屏测试'
        # 查询到的数据是二进制
        json_bytes = self.request.body
        print(json_bytes)
        # 需要进行解码，转成字符串
        json_str = json_bytes.decode('utf-8')
        print(json_str)
        # 在把字符串转换成json字典
        data = json.loads(json_str)
        FlowNum = data.get('FlowNum', '')
        print(FlowNum)
        if FlowNum == '':
            logging.debug('StopFlow post: FlowNum : %s 流程号为空' % FlowNum)
            return HttpResponse('流程号为空')
        flow_num = FlowStatus.objects.filter(flow_num=FlowNum).values()
        print(flow_num)
        FlowName = flow_num[0]['flow_name']
        MachineIp = flow_num[0]['machine_ip']
        print(FlowName)
        logging.info('StopFlow post: 流程名：%s, 机器IP：%s' % (FlowName, MachineIp))
        request_body = [{"Value": "TFlowDM", "Type": 4, "Name": self.IDD_DMName},
                        {"Value": 'zhubh', "Type": 4, "Name": "AppName"},
                        {"Value": '2B710FC391E9413CAFFA048E91120257', "Type": 4, "Name": "AppPass"},
                        {"Value": "ScriptStopFlow", "Type": 4, "Name": self.IDD_lpName},
                        {"Value": FlowName, "Type": 4, "Name": "FlowPath"}
                        ]
        print(request_body)
        resp_data = self.CallFunc(request_body)
        # print(resp_data)
        result = self.parse_json(resp_data, self.IDD_Return)
        if result == '':
            logging.info('StopFlow post: 流程名：%s,停止成功' % FlowName)
        else:
            logging.info('StopFlow post: 流程名：%s, 停止失败，失败信息：%s' % (FlowName, result))
        machine_status = MachineStatus.objects.filter(machine_ip=MachineIp)[0]
        machine_status.machine_status = 0
        machine_status.save()

        return JsonResponse({
            'FlowName': FlowName,
            'result': self.parse_json(resp_data, self.IDD_Return),
        }, status=201)


class Flow_Status(View):
    '''
    查询流程状态
    '''

    def post(self, *args):
        # 查询到的数据是二进制
        json_bytes = self.request.body
        # print(json_bytes)
        # 需要进行解码，转成字符串
        json_str = json_bytes.decode('utf-8')
        print(json_str)
        # 在把字符串转换成json字典
        data = json.loads(json_str.replace('\\', '\\\\'))
        # 获取流程名和流程结果
        FlowNum = str(data.get('FlowNum', ''))

        # 将流程结果保存到FlowStatus中
        try:
            flow = FlowStatus.objects.filter(flow_num=FlowNum).values()[0]
            result = flow['result']
            if result == '成功':
                resultCode = '0000'
            elif result == '正在执行':
                resultCode = '-1'
            else:
                resultCode = '1000'
            data = {"FlowNum": flow['flow_num'], "result": resultCode}
            # response = requests.post(api_flow, data=json.dumps(data))
            logging.info('Flow_Status post: 流程号：%s, 流程结果：%s' % (FlowNum, flow['result']))
            return HttpResponse(json.dumps(data))
        except Exception as e:
            print(e)
            data = {'FlowNum': FlowNum, 'result': e}
            logging.debug('Flow_Status post: 流程号：%s, 不存在' % FlowNum)
        finally:
            return HttpResponse(json.dumps(data))

