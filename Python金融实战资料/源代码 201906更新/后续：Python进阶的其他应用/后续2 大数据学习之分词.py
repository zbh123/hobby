'''Python商业爬虫案例实战后续 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''后续2：大数据学习及分词'''

import jieba
from collections import Counter

# 1.读取文本内容，并利用jieba.cut功能俩进行自动分词
report = open('E:\\领带讲课\\大数据自动分词\\报告.txt', 'r').read()
words = jieba.cut(report)  # 将全文分割，获取到的是一个迭代器，需要通过for循环才能获取到里面的内容

# 2.通过for循环来提取words列表中大于4个字的词语
report_words = []
for word in words:
    if len(word) >= 4:
        report_words.append(word)
print(report_words)

# 3.获得打印输出高频词的出现次数
result = Counter(report_words).most_common(50)  # 取最多的50组
print(result)


