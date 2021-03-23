import win32gui
import win32con
import win32api
import pymouse
import win32clipboard as w
import uiautomation as auto
from time import sleep
import time
import datetime
import pandas as pd
from qq_question import Questioner

auto.uiautomation.SetGlobalSearchTimeout(15)  # 设置全局搜索超时 60
mouse = pymouse.PyMouseMeta()
question_dict = {}  # 记录未回答的问题
LAST_MESS = '测试群设置'
LAST_MESS_TEMP = '测试群设置'


def monitor_click(qq_button):
    """ 模拟点击操作
    :param qq_button:
    :return:
    """
    qq_button.SetFocus()
    qq_button.SendKeys('{Enter}')
    qq_button.SendKeys('{Enter}')
    qq_button.SendKeys('{Enter}')
    qq_button.Click(waitTime=1.5)
    x, y = win32gui.GetCursorPos()
    print(x, y)
    qq_button.SendKeys('{Enter}')
    auto.Click(1696, 1080)


def open_qqbox():
    """ 打开QQ群对话框界面
    :return:
    """
    # 1、任务栏窗口
    task_mainWindow = auto.PaneControl(searchDepth=1, Name='任务栏')
    print(task_mainWindow)
    # 2、通过任务栏窗口获取用户提示通知区域
    warn_part = task_mainWindow.ToolBarControl(Name="用户提示通知区域")
    print(warn_part)
    # 3、获取并点击QQ按钮
    qq_button = warn_part.ButtonControl(foundIndex=2, searchDepth=1)
    # QQ名称 = '''QQ: 祝佰航(990095293)\r\n声音: 关闭\r\n消息提醒框: 关闭\r\n会话消息: 任务栏头像闪动'''
    # qq_button = warn_part.ButtonControl(Name=QQ名称, searchDepth=1)
    print(qq_button)
    qq_button.Click(waitTime=1.5)
    sleep(0.5)
    # 获取并激活QQ界面
    main_window = auto.WindowControl(searchDepth=1, Name='QQ')
    main_window.SetActive()
    print(main_window)
    sleep(0.5)
    # 获取搜索框
    search_Edit = main_window.EditControl(searchDepth=6, Name="搜索：联系人、群聊、企业")
    sleep(0.5)
    # 搜索群名称
    search_Edit.SetFocus()
    search_Edit.SendKeys('中泰证券二部技术讨论')
    search_Edit.SendKeys('{Enter}')
    sleep(0.5)
    # 最大化打开的对话框
    dialog_box = auto.WindowControl(Name='中泰证券二部技术讨论', searchDepth=1)
    print(dialog_box)
    dialog_box.Maximize()


def gettext():
    """ 获取剪切板的内容
    :return:
    """
    w.OpenClipboard()
    t = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return t


def save_content(LAST_MESS_TEMP):
    """ 复制聊天记录到指定文件中
    :return:
    """
    dialog_box = auto.WindowControl(Name='中泰证券二部技术讨论', searchDepth=1)
    dialog_box.SetActive()
    dialog_box.Maximize()
    message_win = dialog_box.ListControl(Name='消息', searchDepth=13)
    message_win.Click()
    auto.Click(800, 800)
    message_win.SendKeys('{Ctrl}A')
    message_win.SendKeys('{Ctrl}C')
    df = pd.read_clipboard(sep=r"\s+", encoding='utf-8', error_bad_lines=False)
    df.to_csv('message_tmp.txt', index=False, sep=' ', encoding='utf_8_sig')
    # 查找未写入文件的内容
    k = 0
    with open('message_tmp.txt', 'r', encoding='utf_8_sig') as fp:
        readlines = fp.readlines()
        for i, line in enumerate(readlines):
            if line == LAST_MESS_TEMP:
                k = i
                break
        LAST_MESS_TEMP = readlines[-1].strip()

    # 将未写入文件的内容写入文件
    with open('message.txt', 'a+', encoding='utf_8_sig') as fp:
        readlines = fp.readlines()
        for i in range(k, len(readlines)):
            fp.write(readlines[i])
    return LAST_MESS_TEMP


def reply(author, result):
    """ 回复消息
    :param author:
    :param result:
    :return:
    """
    dialog_box = auto.WindowControl(Name='中泰证券二部技术讨论', searchDepth=1)
    dialog_box.SetActive()
    input_win = dialog_box.ListControl(Name='消息', searchDepth=13)
    input_win.Click()
    user = '@' + author
    input_win.SendKeys(user)
    input_win.SendKeys('{Enter}')
    input_win.SendKeys(result)
    send_button = dialog_box.ButtonControl(Name="发送(&S)", searchDepth=13)
    print(send_button)
    # send_button.Click()


def convert_hms_s(time_str):
    ''' 将时分秒转成秒
    :param time_str:
    :return:
    '''
    hour, min, sec = time_str.strip().split(':')
    second = int(hour) * 3600 + int(min) * 60 + int(sec)
    return second


def read_files(LAST_MESS):
    # utf_8_sig这种编码格式为了去掉字段前面的8进制空格\ufeff
    with open('message.txt', 'r', encoding='utf_8_sig') as fp:
        readlines = fp.readlines()
    k = 0
    # 记录上一次读取的位置
    for i, line in enumerate(readlines):
        if line == LAST_MESS:
            k = i
            break
    delete_author_list = []
    # 遍历未回答的问题，优先处理这类问题
    for key, values in question_dict.items():
        for i in range(k, len(readlines)):
            lines = readlines[i]
            if lines.startswith(key):
                if i == len(readlines) - 1:    # 最后一行
                    pass
                delete_author_list.append(key)
                question_line = readlines[i + 1]
                ques = values
                ques.update_question(question_line)
                result = ques.get_answer()
                reply(key, result)
                ques.set_status(False)
                if not ques.result:
                    del ques
                break

    # 超过15分钟未找到问题的类
    for author, obj in question_dict.items():
        start_time = obj.time_q
        start_sec = convert_hms_s(start_time)
        now_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
        print(now_time)
        end_sec = convert_hms_s(now_time)
        use_time = end_sec - start_sec
        if use_time > 900:
            delete_author_list.append(author)

    # 从字典中删除已回答或超时的项
    for author in delete_author_list:
        question_dict.pop(author, 'None')


    # 从上次阅读的地方开始，遍历文件，查找问题
    for i in range(k, len(readlines)):
        line = readlines[i]
        # print(line)
        # 第一次运行时直接执行，如果有人@，继续
        if '@' in line:   # line是@所在行
            print(line)
            que = readlines[i - 1]    # 提问者信息所在行
            print(readlines[i - 1])
            author_line = que.strip().split()    # 解析提问者信息
            print(author_line)
            # current_time = datetime.datetime.now().strftime("%Y-%m-%d %X")
            # current_day = datetime.datetime.now().strftime("%Y-%m-%d")
            if len(author_line) != 2:      # 提问者信息中当天所在信息只有两行，历史记录有3行（年月日）
                print('不是当天时间')
                continue

            question_line = line.strip().split()    # 解析@所在行
            time_q = " ".join(x for j, x in enumerate(author_line) if j != 0)  # 提问者记录时间
            print(time_q)
            author = author_line[0]       # 记录提问者
            print(author)
            question = ''
            if len(question_line) < 2:     # @所在行没有问题时，遍历之后的文件查找问题
                for j in range(i + 1, len(readlines)):
                    if readlines[j].strip().startswith(author):
                        question = readlines[j + 1]
                        break
                if question == '':
                    print('未发现提问者提问题')
            else:      # @所在行有问题时
                question = " ".join(x for j, x in enumerate(question_line) if j != 0)
                print(question)
            question_answer(author, question, time_q)    # 回答问题
        if i == len(readlines) - 1:
            LAST_MESS = line          # 记录当前文件最后一行
    return LAST_MESS


def question_answer(author, question, time_q):
    """ 回答提问者提出的问题
    :param author:
    :param question:
    :param time_q:
    :return:
    """
    ques = Questioner(author, question, time_q, True)     # 具体化对象
    if question != '':           # 问题存在时
        result = ques.get_answer()
        reply(author, result)
        ques.set_status(False)
    else:                       # 问题不存在时，写入字典
        if author not in question_dict:
            question_dict[author] = ques

    if not ques.result:     # 删除已回答问题的class
        del ques


# open_qqbox()
# LAST_MESS_TEMP = save_content(LAST_MESS_TEMP)
# LAST_MESS = read_files(LAST_MESS)
# reply('祝佰航', '测试')
if __name__ == '__main__':
    open_qqbox()
    LAST_MESS_TEMP = save_content(LAST_MESS_TEMP)
