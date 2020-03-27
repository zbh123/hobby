//BOM是浏览器对象，主要是与浏览器相关，用于访问浏览器和计算机屏幕的对象集合

//window.document表示的是当前载入的文档（即页面）也就是页面HTML的所有内容

//window.frames 是当前页面所有框架的集合（基本不用）

//window.navigator用于反应浏览器及其功能信息的对象（接受发送的信息）

//window.screen提供浏览器以外的环境信息（屏幕的信息,大小等）

//window.location
//href() 控制浏览器地址栏的内容
//reload() 刷新页面
//reload(true)刷新页面，不带缓存
//assign() 加载新的页面
//replace() 加载新的页面，并不会在浏览器的历史记录中留下记录
function func(){
    window.location.href = 'http://www.baidu.com'
}
function refresh(){
    window.location.reload()
}
function ass(){
    window.location.assign = 'http://www.baidu.com'
}

//window.history  历史记录
//window.history.length  获取历史记录的长度
//back() 上一页
//forward() 下一页
//go(num) 跳转到num页

function backPage(){
    window.history.back();
}
//window的方法
//打开新的页面，包含的参数，跳转的页面，是否新开页面（打开一个新的页面），设置页面的样式
window.open('*.html',"blank", "width=100px, height=100px, left=0px, top=0px")
//关闭当前页面
window.close()
//页面加载成功触发该事件
window.onload() = function(){
    alert('看看')
}
//页面卸载成功触发该事件，当前页面切换
window.onunload() = function(){
    alert('看看')
}
//滚动触发事件
window.onscroll = function(){
    alert('页面滚动')
    //获取当前页面的滚动值，先试着获取||前面的表达式的值，获取不到再拿后面表达式的值
    var a = document.documentElement.scrollTop || document.body.scrollTop
    console.log(a)
    if(a==500*i){
    //加载新数据
    }
}
//页面size改变触发事件
window.onresize = function(){
    var w = document.documentElement.clientWidth || document.body.clientWidth || window.innerWidth
    var h = document.documentElement.clientHeight || document.body.clientHeight || window.innerHeight
    console.log(w,h)
}
//间歇性定时器,2000是毫秒
var time = window.setInterval(function(){
    console.log('定时')
},2000)
function func1(){
    //清除定时器
    window.clearInterval(time)
}
function func2(){
    var time = window.setInterval(function(){
        console.log('定时')
    },2000)
    }

//与当前时间间隔3s再执行
var time = window.setTimeout(function(){
    console.log('定时器')
},3000)










