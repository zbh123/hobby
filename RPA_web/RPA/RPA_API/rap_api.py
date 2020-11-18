#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from urllib import request
import json
import os
import configparser

global FsServerIP
global FsPort
global AomFile
global FlowName
ConfigFile = os.path.join(os.path.dirname(__file__), 'rpa_api.ini').replace('/', '\\')
conf = configparser.ConfigParser()
conf.read(ConfigFile, encoding='utf-8')

try:
    FsServerIP = conf.get('RPAInfo', 'Host')
    FsPort = conf.get('RPAInfo', 'Port')
    AomFile = conf.get('RPAInfo', 'AomScriptPath')
    FlowName = conf.get('RPAInfo', 'FlowName')
    print(FlowName)
except:
    print('读取配置文件失败')
    os._exit(-1)
# FsServerIP = "10.29.132.76"
# FsPort = "12580"
# FsRemoteID = "9540DCDA7AF74233ABF677401C05DEA4"

REQUEST_URL = "http://%s:%s/CallFunc.aom" % (FsServerIP, FsPort)  # 请求地址

IDD_Return = "{50043442-8A69-4A6B-A8B5-61F882EDE4F3}"  # 返回消息
IDD_DMName = "{9F8E5ECB-5976-4315-B8F3-43B8502B694D}"  # 类文件
IDD_lpName = "{2881E26D-62CE-4937-B4BB-8998440417C4}"  # 方法
IDD_GlobalID = "{9D81EE66-3CD3-428B-BB3A-F67111F70CAE}"  # GlobalID
IDD_Message = "{BBA7501B-B7A9-492A-96EC-4E44C310832C}"  # 消息

WM_USER = 0x7a68756268


def readInifile():
    '''读取配置文件'''
    content = conf.read(ConfigFile)
    try:
        FsServerIP = content['RPAInfo']['Host']
        FsPort = content['RPAInfo']['Port']
        AomFile = content['RPAInfo']['AomScriptPath']
    except:
        print('读取配置文件失败')
        os._exit(-1)


def CallFunc(url, body):
    '''请求后台'''
    try:
        if url == "":
            return "Path cannot be empty"

        req = request.Request(url, data=json.dumps(body).encode('gbk'))
        f = request.urlopen(req)
        try:
            return f.read()
        finally:
            f.close()
    except Exception as e:
        return str(e)


def parse_json(json_data, value_name="Value"):
    '''解析json返回值'''
    try:
        for jdata in json.loads(json_data, strict=False):
            if jdata["Name"] == IDD_Return:
                return jdata["Value"]
            if jdata["Name"] == value_name:
                return jdata["Value"]
        return json.loads(json_data, strict=False)
    except Exception as e:
        return str(e)


def runFlow():
    '''执行流程'''
    # sName = r'测试\录屏测试'
    # request_body = [{"Value": "TFlowDM", "Type": 4, "Name": IDD_DMName},
    #                 {"Value": 'zhubh', "Type": 4, "Name": "AppName"},
    #                 {"Value": '2B710FC391E9413CAFFA048E91120257', "Type": 4, "Name": "AppPass"},
    #                 {"Value": "ScriptStartFlow", "Type": 4, "Name": IDD_lpName},
    #                 {"Value": FlowName, "Type": 4, "Name": "FlowPath"}
    #                 ]
    request_body = [{"Value": "TSchedulerDM", "Type": 4, "Name": IDD_DMName},
                    {"Value": 'zhubh', "Type": 4, "Name": "AppName"},
                    {"Value": '2B710FC391E9413CAFFA048E91120257', "Type": 4, "Name": "AppPass"},
                    {"Value": "SetTaskInfo", "Type": 4, "Name": IDD_lpName},
                    {"Value": FlowName, "Type": 4, "Name": "Name"},
                    {"Value": '16:03:00', "Type": 4, "Name": "ExceTime"},
                    {"Value": '2020-11-17', "Type": 4, "Name": "ExceDate"},
                    {"Value": '2020-11-17 16:03:00', "Type": 4, "Name": "BeginTim"}
                    ]
    # print(request_body)
    resp_data = CallFunc(REQUEST_URL, request_body)
    # print(resp_data)
    print(parse_json(resp_data, IDD_Return))


if __name__ == '__main__':
    # getFsRemoteID()
    runFlow()
