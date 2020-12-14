#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import paramiko
from functools import wraps
from datetime import datetime


def timethis(func):
    """
    时间装饰器，计算函数执行所消耗的时间
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        print(func.__name__, end - start)
        return result

    return wrapper


class SSHManager:
    def __init__(self, host, usr, passwd):
        self._host = host
        self._usr = usr
        self._passwd = passwd
        self._ssh = None
        self._sftp = None
        self._sftp_connect()
        self._ssh_connect()

    def __del__(self):
        if self._ssh:
            self._ssh.close()
        if self._sftp:
            self._sftp.close()

    def _sftp_connect(self):
        try:
            transport = paramiko.Transport((self._host, 222))
            transport.connect(username=self._usr, password=self._passwd)
            self._sftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            raise RuntimeError("sftp connect failed [%s]" % str(e))

    def _ssh_connect(self):
        try:
            # 创建ssh对象
            self._ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            self._ssh.connect(hostname=self._host,
                              port=222,
                              username=self._usr,
                              password=self._passwd,
                              timeout=5)
        except Exception:
            raise RuntimeError("ssh connected to [host:%s, usr:%s, passwd:%s] failed" %
                               (self._host, self._usr, self._passwd))

    def ssh_exec_cmd(self, cmd, path='~'):
        """
        通过ssh连接到远程服务器，执行给定的命令
        :param cmd: 执行的命令
        :param path: 命令执行的目录
        :return: 返回结果
        """
        try:
            result = self._exec_command('cd ' + path + ';' + cmd)
            print(result)
        except Exception:
            raise RuntimeError('exec cmd [%s] failed' % cmd)

    def ssh_exec_shell(self, local_file, remote_file, exec_path):
        """
        执行远程的sh脚本文件
        :param local_file: 本地shell文件
        :param remote_file: 远程shell文件
        :param exec_path: 执行目录
        :return:
        """
        try:
            if not self.is_file_exist(local_file):
                raise RuntimeError('File [%s] not exist' % local_file)
            if not self.is_shell_file(local_file):
                raise RuntimeError('File [%s] is not a shell file' % local_file)

            self._check_remote_file(local_file, remote_file)

            result = self._exec_command('chmod +x ' + remote_file + '; cd' + exec_path + ';/bin/bash ' + remote_file)
            print('exec shell result: ', result)
        except Exception as e:
            raise RuntimeError('ssh exec shell failed [%s]' % str(e))

    @staticmethod
    def is_shell_file(file_name):
        return file_name.endswith('.sh')

    @staticmethod
    def is_file_exist(file_name):
        try:
            with open(file_name, 'r'):
                return True
        except Exception as e:
            return False

    def _check_remote_file(self, local_file, remote_file):
        """
        检测远程的脚本文件和当前的脚本文件是否一致，如果不一致，则上传本地脚本文件
        :param local_file:
        :param remote_file:
        :return:
        """
        try:
            result = self._exec_command('find' + remote_file)
            if len(result) == 0:
                self._upload_file(local_file, remote_file)
            else:
                lf_size = os.path.getsize(local_file)
                result = self._exec_command('du -b' + remote_file)
                rf_size = int(result.split('\t')[0])
                if lf_size != rf_size:
                    self._upload_file(local_file, remote_file)
        except Exception as e:
            raise RuntimeError("check error [%s]" % str(e))

    @timethis
    def _upload_file(self, local_file, remote_file):
        """
        通过sftp上传本地文件到远程
        :param local_file:
        :param remote_file:
        :return:
        """
        try:
            self._sftp.put(local_file, remote_file)
        except Exception as e:
            raise RuntimeError('upload failed [%s]' % str(e))

    def _exec_command(self, cmd):
        """
        通过ssh执行远程命令
        :param cmd:
        :return:
        """
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            return stdout.read().decode()
        except Exception as e:
            raise RuntimeError('Exec command [%s] failed' % str(cmd))


if __name__ == '__main__':
    ip = '192.168.159.142'
    usr = 'leo'
    passwd = '123'
    ssh = SSHManager(ip, usr, passwd)
    ssh.ssh_exec_cmd('ls')
    ssh.ssh_exec_shell('./test.sh', '/home/leo/test.sh', '/home/leo')