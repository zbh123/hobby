'''

作用：收集用户信息
表单组成：
    表单域
    表单控件
    提示信息

表单域：
语法：<form 属性名称=“value”>

常用属性：
name='';规定表单的名称
action='';提交表单url
method='get/post'：提交方式
enctype='' 规定在发送表单数据之前进行编码
target='_black/_self/_parent/_top';何处打开表单url
H5新增属性：
autocomplete='on/off';是否启动表单自动完成
novalidate='novalidate';不验证表单
float:left/right 浮动
表单控件
1、文本框 <input type='text' values='设置默认值'
2、密码框<input type='password' placeholder='密码'
3、提交按钮<input type='submit' value='按钮名称'
4、重置按钮<input type='reset' value='按钮名称'
5、单元框/单选按钮<input type='radio' name='****' checked='checked'
6、按钮<input type='button' value='按钮名称'
7、复选框<input type='checkbox' name='***' disabled='disabled'
8、下拉菜单<select name='***'>
                <option> 菜单内容
9、多行文本框<textarea name='**' cols='字符宽度' rows='行数'

高级表单
<filedset>
    <legend

label 绑定表单，鼠标点击文字，进入相应文本框
'''