import os
import psutil
from time import sleep
import sys
import subprocess


def get_pid(name):
    process_name = os.path.basename(name)
    print(process_name)
    all_pid = psutil.pids()
    for sub_id in all_pid:
        process = psutil.Process(sub_id)
        if process_name == process.name():
            print('进程存在')
            sleep(1)
            return True
    return False


def kill_pid(name):
    process_name = os.path.basename(name)
    print(process_name)
    all_pid = psutil.pids()
    for sub_id in all_pid:
        process = psutil.Process(sub_id)
        if process_name == process.name():
            print('进程已存在, 3s后自动关闭进程')
            sleep(3)
            # print(process.terminate())
            # sleep(2)
            # get_pid(name)
            print('taskkill /f /im %s' % process_name)
            os.popen('taskkill /f /im %s' % process_name)
            return False
    return True


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    print('ready to restart program......')
    python = sys.executable
    print(python)
    os.execl(python, __file__, *sys.argv)


while True:
    py_path = r'C:\Users\zhubh\AppData\Local\Programs\Python\Python36\python.exe'
    cmd_path = r'C:\Windows\System32\cmd.exe'
    if get_pid(py_path) and get_pid(cmd_path):
        sleep(1)
        pass
    else:
        # kill_pid(py_path)
        # kill_pid(cmd_path)
        dir_file = os.path.dirname(__file__)
        # manage_file = (os.path.join(dir_file, 'runserver.bat')).replace('\\', '/')
        manage_file = r'D:\pyfile\github_files\hobby\RPA_web\RPA\runserver.bat'
        try:
            subprocess.Popen('%s' % manage_file, shell=True)
            # os.system('python manage.py runserver 0:8080')
        except Exception as e:
            print(e)
            restart_program()
        finally:
            pass
