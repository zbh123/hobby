# coding:utf-8


class Questioner():
    def __init__(self, author, question, time_q, status):
        self.author = author      # 提问者
        self.question = question  # 问题
        self.time_q = time_q  # 提问时间
        self.result = status

    def get_answer(self):
        ''' # 调用提供的方法，获取回答
        :return:
        '''
        result = self.question
        return result

    def set_status(self, status):
        ''' 设置当前类的状态，False：已经结束，True：进行中
        :param result:
        :return:
        '''
        self.status = status
        return self.status

    def update_question(self, question):
        self.question = question



