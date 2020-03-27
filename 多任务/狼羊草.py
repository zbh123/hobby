import itertools
'''
想要实现的功能是，智能的选择过河的顺序
'''

def is_valid_status(status):
    if status[1] == status[2] and status[0] != status[1]:
        print('狼吃羊')
        return False
    if status[2] == status[3] and status[0] != status[2]:
        print('羊吃草')
        return False
    return True


def create_all_next_status(status):
    '''
    一种状态的下面会有多种子状态，将合理的子状态全部输出
    :param status:
    :return:
    '''
    next_status_list = []

    for i in range(0,4):
        if status[0] != status[i]:
            continue
        next_status = [not status[0], status[1], status[2],status[3]]
        next_status[i] = next_status[0]

        if is_valid_status(next_status):
            next_status_list.append(next_status)
    return next_status_list

def is_done(status):
    return status[0] and status[1] and status[2] and status[3]

def readable_status(status, is_across):
    result = ''
    for i in range(0,4):
        if status[i] == is_across:
            if len(result) != 0:
                result += ","
            result += name[i]
    return "[" + result + "]"

def print_history_status(history_status):
    for status in history_status:
        print('%s=======%s'%(readable_status(status, False), readable_status(status, True)))

def search(history_status):
    global scheme_count

    current_status = history_status[len(history_status)-1]

    next_status_list = create_all_next_status(current_status)
    print(len(next_status_list))
    for next_status in next_status_list:
        print(next_status)
        if next_status in history_status:
            continue
        history_status.append(next_status)
        #判断是否完成
        if is_done(next_status):
            scheme_count += 1
            print_history_status(history_status)
        else:
            search(history_status)
        history_status.pop()

if __name__ == '__main__':
    #初始化开局，都没到对岸
    name = ['farmer','wolf','sheep','grass']
    scheme_count = 0
    status = [False, False, False, False]
    #历史局面列表
    history_status = [status]
    search(history_status)
    print('finish search, find' + str(scheme_count) + ' scheme')





