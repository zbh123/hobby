'''2 正则表达式详解 by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释后运行

'''2.4 自动考虑换行re.S方法'''
import re
res = '''<h3 class="c-title">
 <a href="http://news.sina.com.cn/o/2018-12-12/doc-ihqackaa4351174.shtml"
    data-click="{
      'f0':'77A717EA',
      'f1':'9F63F1E4',
      'f2':'4CA6DD6E',
      'f3':'54E5343F',
      't':'1544622684'
      }"

                target="_blank"

    >
      <em>阿里巴巴</em>电商脱贫成“教材” 累计培训逾万名县域干部
    </a>
'''
p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
p_title = '<h3 class="c-title">.*?>(.*?)</a>'
href = re.findall(p_href, res, re.S)
title = re.findall(p_title, res, re.S)
print(href)
print(title)