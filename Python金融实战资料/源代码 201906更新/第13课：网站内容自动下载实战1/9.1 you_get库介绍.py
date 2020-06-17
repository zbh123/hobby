'''Python商业爬虫案例实战第9节：网站内容自动下载实战1 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''9.1节：you_get库介绍'''
'''1.1.保存到电脑的默认文件夹'''
#原始写法
# import os
# os.system('you-get http://p99.pstatp.com/origin/tuchong.fullscreen/227148277_tt')

#改进写法，不要忘了空格
import os
url = 'http://p99.pstatp.com/origin/tuchong.fullscreen/227148277_tt'
os.system('you-get ' + url)

'''1.2 自定义储存位置'''
#原始写法
# import os
# os.system('you-get -o D:\\我的图片 http://p99.pstatp.com/origin/tuchong.fullscreen/227148277_tt')

#改进写法
import os
directory = 'D:\\我的图片'
url = 'http://p99.pstatp.com/origin/tuchong.fullscreen/227148277_tt'
os.system('you-get -o ' + directory + ' ' + url)


'''1.3 自定义文件保存名字'''
# 原始写法
import os
os.system('you-get -o D:\\我的图片 -O 新名字 http://p99.pstatp.com/origin/tuchong.fullscreen/227148277_tt')

#改进写法
import os
directory = 'D:\\我的图片'
name = '新的名字'
url = 'http://p99.pstatp.com/origin/tuchong.fullscreen/227148277_tt'
os.system('you-get -o ' + directory + ' -O ' + name + ' ' + url)


'''1.4 练习：爬取PDF文件'''
#修改保存视频的名字
import os
directory = 'D:\\我的图片'
name = '万科年报'
url = 'http://disc.static.szse.cn/download/disc/disk01/finalpage/2018-08-21/64ef0b06-43b7-40e4-b331-b07d0283c924.PDF'
os.system('you-get -o ' + directory + ' -O ' + name + ' ' + url)
