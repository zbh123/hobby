# !/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'zhubh'
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.http import JsonResponse
import datetime
from urllib import request
import json
import os
import pretty_errors

# Create your views here.
pretty_errors.activate()


class StartFlow(View):

    def __init__(self):
        self.AomFile = r'C:\Users\zhubh\Desktop\agent\Temp\Temp\AomScript.py'
        self.FsServerIP = '10.29.132.76'
        self.FsPort = '12580'
        self.REQUEST_URL = "http://%s:%s/CallFunc.aom" % (self.FsServerIP, self.FsPort)  # 请求地址
        self.IDD_Return = "{50043442-8A69-4A6B-A8B5-61F882EDE4F3}"  # 返回消息
        self.IDD_DMName = "{9F8E5ECB-5976-4315-B8F3-43B8502B694D}"  # 类文件
        self.IDD_lpName = "{2881E26D-62CE-4937-B4BB-8998440417C4}"  # 方法
        self.IDD_GlobalID = "{9D81EE66-3CD3-428B-BB3A-F67111F70CAE}"  # GlobalID
        self.IDD_Message = "{BBA7501B-B7A9-492A-96EC-4E44C310832C}"  # 消息

    def getToken(self):
        '''获取token'''
        with open(self.AomFile, 'r') as fp:
            content = fp.readlines()
        for line in content:
            if line.startswith('FsRemoteID = '):
                print(line.split('FsRemoteID = ')[-1].strip())
                FsRemoteID = line.split('FsRemoteID = ')[-1].strip().replace('"', '')
                return FsRemoteID
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
        FlowName = data.get('FlowName', '')
        print(FlowName)
        if FlowName == '':
            return HttpResponse('流程名称为空')
        request_body = [{"Value": "TFlowDM", "Type": 4, "Name": self.IDD_DMName},
                        {"Value": self.getToken(), "Type": 4, "Name": "Token"},
                        {"Value": "ScriptStartFlow", "Type": 4, "Name": self.IDD_lpName},
                        {"Value": FlowName, "Type": 4, "Name": "FlowPath"}
                        ]
        print(request_body)
        resp_data = self.CallFunc(request_body)
        # print(resp_data)
        print(self.parse_json(resp_data, self.IDD_Return))

        return JsonResponse({
            'flow_name': FlowName,
            'result': self.parse_json(resp_data, self.IDD_Return),
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
