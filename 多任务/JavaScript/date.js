//<!--只显示当前时间-->
var d1 = Date()
//<!--新建时间变量，可以自己设置时间-->
var d2 = new Date()
var d3 = new Date("2017-10-01")
var d4 = new Date(2017,1,2,15,12,12)

//获取年份
date.getFullYear()
//获取月份，0表示1月份
date.getMonth()
//获取日期
date.getDate()
//获取星期
date.getDay()
//获取小时
date.getHours()
//获取分钟
date.getMinutes()
//获取秒数
date.getSeconds()

//设置年份，同上
date.setFullYear(2015)

//转换成字符串
//包含年月日时分秒
date.toLocaleString()
//包含年月日
date.toLocalDateString()
//包含时分秒
date.toLocalTimeString()
//返回该日期距离1970年1月1日0点的毫秒数
Date.parse("2016-10-10")
//日期相减是两个日期间隔的时间戳，相加是两个字符串相加







