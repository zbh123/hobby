'''2 正则表达式详解 by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释后运行

'''2.2 非贪婪匹配(.*?)'''
import re
res = '<p class="c-author">新浪新闻&nbsp;&nbsp; 5小时前</p>'
p_source = '<p class="c-author">(.*?)&nbsp'
source = re.findall(p_source, res)
print(source)

'''
逐行释义：
1.引入正则表达式库
2.文本内容res 为 '<p class="c-author">新浪新闻&nbsp;&nbsp; 5小时前</p>'
3.匹配规则为p_source：'<p class="c-author">(.*?)&nbsp'
4.使用findall在res中寻找满足左边是<p class="c-author">右边是&nbsp的内容
5.打印source变量
'''

import re
res = '<p class="c-author">新浪新闻&nbsp;&nbsp; 5小时前</p><p class="c-author">微信推文&nbsp;&nbsp; 2小时前</p><p class="c-author">人民网&nbsp;&nbsp; 3小时前</p><p class="c-author">今日头条&nbsp;&nbsp; 10小时前</p>'
p_source = '<p class="c-author">(.*?)&nbsp'
source = re.findall(p_source, res)
print(source)