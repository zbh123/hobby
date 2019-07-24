#include<stdio.h>
#include<time.h>

int main(){
//定义时间类型的ptr
 struct tm *ptr;
 //定义时间
 time_t t;
 //获取当前时间，秒数
 t = time(NULL);
 //将当前时间转化成格林尼治时间
 ptr = gmtime(&t);
 //asc格式打印格林尼治时间
 printf(asctime(ptr));
 //打印本地时间
 printf(ctime(&t));
 printf("UTC hour is %d\n",ptr->tm_hour);
 printf("UTC day is %d\n",ptr->tm_mday);
 
 struct tm *local;
 time_t it;
 it = time(NULL);
 local = localtime(&it);
 printf("Local hour is %d", local->tm_hour);

}



