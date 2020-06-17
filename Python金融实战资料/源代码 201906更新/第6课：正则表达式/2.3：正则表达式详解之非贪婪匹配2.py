'''2 正则表达式详解 by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释后运行

'''2.3 非贪婪匹配.*?'''
import re
res = '<h3 class="c-title"><a href="http://news.hexun.com/2018-12-12/195521925.html" data-click="{一堆英文}"><em>阿里巴巴</em>电商脱贫成“教材” 累计培训逾万名县域干部</a>'
p_title = '<h3 class="c-title">.*?>(.*?)</a>'
title = re.findall(p_title, res)
print(title)
