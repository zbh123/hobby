console.log("在外面的js文件中")

//没有用var定义的变量，默认为全局变量

//数字部分
var num;
num = 'a';
console.log(num)

var num1 = 10;
var num2 = 10;
var num = num1 + num2;
console.log("sum = " + sum.toString()) //转换成字符


var num5 = 1e309  //科学计数法
var num6 = Infinity
var num6 = NaN   //表示不是数，但是数字类型的
console.log(Infinity)
console.log(typeof(NaN))
console.log(NaN == NaN)  //返回False
console.log(isNaN(NaN))  //返回True

//字符串类型

var str1 = "hehe"
//字符串+数字，先将数字转成字符串

console.log(str1 + '!')
console.log(typeof(str1))
//布尔值
var b = true
var c = false

//真假值 0， 0.0， “”, NaN, undefined, null为假，其余为真

//字符串转数字,parseInt从开头开始，直到遇到非数字字符
var a = '123'
var num7 = parseInt(a)

var num8 = parseInt(prompt('请输入一个数字'))

var num9 = 10
var num10 = 10
//前后++都是给数加1，后++的值是num的值（先赋值在+1），前++的值是num+1的值（先+1再赋值）
console.log(num9++)
console.log(num9)
console.log(++num10)
console.log(num10)

#==是相等，===绝对相等（类型数值相等）

//while语句

var num11 = 1;
var sum = 0;
while (num<10){
    sum += num;
    num++;
}
//do....while....先执行do语句

var sum1 = 0;
var num12 = 1;
do {
        sum+=num12
        num12++
} while(num<10){
    console.log(sum)
}

//for语句

var sum2 = 0;
for(var num=1; num<=10; num+=1){
    sum+=num;
    }
//for的死循环
for(;;){
    console.log('1111');
}

//for....in....遍历数组或对象的元素

var lis1 = [1,2,3,4,5,6,7,8,9]

for(var i=1; i<10; i++){
    for(var j=1; j<10; j++){
        console.log(i*j)
    }
}

//函数结构
'''
function 函数名(参数列表){
    语句
    return 表达式
}
''''
function func(){
    console.log('he')
}

//调用
func()

//如果实参传的过多，函数依然可以使用
function func(num1, num2){
    console.log(arguments.length)
    for(var i = 0; i<arguments.length; i++)
    console.log(arguments[i])
    console.log('he' + num1 + num2)
}
func(1,2,3,4,5,6,7)

//函数的另一种表示方法

var f = function(a,b){
    return a+b
}
f(1,2)//调用
//即时函数
(function(str){
    console.log(str)
})('即时函数参数')

//列表数组

var arr = [1,2,3,4,5]
for(var i = 0; i<arr.length; i++){
    console.log('arr[%d] = %d', i, arr[i])
}
for (var i in arr){
    console.log('arr[%s] = %d', i, arr[i])
}

//创建空数组
var arr1 = new Array()
#创建数组，包含多种类型
var arr2 = new Array(1,2,'safe')
//只有一个参数时，定义数组长度为10，可以扩展，不限个数
var arr2 = new Array(10)
//可以使用delete删除数组的值，但不能删除位置，即删除值后，该位置的值为undefined

//匿名函数遍历数组
var arr3 = new Array(5)
arr3[0] = 0;
arr3[1] = 1;
arr3[2] = 2;
arr3[3] = 3;
arr3[4] = 4;
arr3[5] = 5;
arr3.forEach(function(item)){
    console.log(item)
}

//向数组中添加元素
//从后面添加元素
arr3.push(6)
//从前面添加元素
arr3.unshift(7)
//删除元素，从后面拿
arr3.pop()
//删除元素，从前面拿
arr3.shift()
//字符串拼接，数列之间以&拼接在一起
arr3.join("&")
//反转列表
arr3.reverse()
//切片
var arr4 = arr3.slice(1,3)
// 8    splice插入或删除元素splice(下标，个数，item1， item2)
//必须的参数下标和个数
//功能在数组中间插入或删除数组元素，插入的话，个数为0，返回被删除的数组
//splice插入方式，在下标为2的地方，插入8,9两个数
var arr5 = arr3.splice(2,0,8,9)
//删除方式,删除从下标1开始的3个数据
var arr6 = arr3.splice(1,3)
//替换方式,替换从下标1开始的3个数据
var arr6 = arr3.splice(1,3,10,20,30)


// 9   拼接数组
var arr7 = arr3.contact(arr4,arr5)

// 10 indexOf 查找，从数组头部查找数组元素，找到返回数组元素的下标，否则返回-1
var arr10 = arr7.indexOf(3)
// 10 lastindexOf 查找，从数组尾部查找数组元素，找到返回数组元素的下标，否则返回-1
var arr10 = arr7.indexOf(3)



//冒泡排序
var arr11 = [5,3,2,6,1]
for (var i = 0; i <arr11.length - 1; i++){
    for(var j = 0; j < arr11.length - 1 - i; j++){
        if (arr11[j] > arr11[j+1]){
            var temp = arr11[j];
            arr11[j] = arr11[j+1];
            arr11[j+1] = temp;
        }
    }
}
//字符串排序算法sort
arr11.sort(function(x,y){
    return x.length > y.length
})


//定义字符串
var str = new String('he') //object类型的
var str = 'he' //字符串类型的
//1、charAt(index),获取指定下标的字符
str.charAt(2)

//2、charCodeAt(index)，获取指定下标的字符串的ASCII码，返回值为0~65535之间的整数
console.log(str.charCodeAt(2))
//3、String.fromCharCode（ASCII码）将ASCII码转换成对应的字符
var str2 = String.fromCharCode(97)
//4、字符串大小写转换，返回转换后的字符串
//toLowerCase全部转成小写和toUpperCase转成大写
var str3 = str2.toLowerCase();

//5、判断是否相等==,===,或localeCompare（返回1或0）
str2.localeCompare(str3)
//indexOf查找字符
str2.indexOf('h')
//替换字符，replace(要替换的字符，替换后的字符)
var str4 = str2.replace('he', 'heheh')
//提取子串，从index为9到11的子串
var str5 = str.substring(9,11)
//index为9之后的所有字符
var str5 = str.substr(9)

//字符串分割split同Python的split,合并数组用join编程字符串
var str6 = str.split(' ')

//Math对象
//四舍五入
Math.round(3.6)
//向上取整
Math.ceil(3.6)
//向下取整
Math.floor(3.6)
//取最大值
Math.max(3.6)
//取最小值
Math.min(3.6)
//绝对值
Math.abs(3.6)
//x的y次方（x=3，y6）
Math.pow(3，6)
//开平方
Math.sqrt(3.6)
//随机输出x-y之间的一个整数（包含x，y）
//0-100的随机数
Math.random() * 100
//公式 Math.random() * (y - x + 1) + x
Math.random() * (6-2+1)+2




