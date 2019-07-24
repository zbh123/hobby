#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>

int sharei = 0;
void num_cal(void);

//定义线程锁
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

int main(){
//定义多个线程
 pthread_t thr1, thr2, thr3;
 //创建各线程
 pthread_create(thr1, NULL, num_cal, NULL);
 pthread_create(thr2, NULL, num_cal, NULL);
 pthread_create(thr3, NULL, num_cal, NULL);
//开始各线程
 pthread_join(thr1, NULL);
 pthread_join(thr2, NULL);
 pthread_join(thr3, NULL);
 
 printf("the finally shreai is %d", sharei);
}

void num_cal(){
 int i;
 //给线程加锁
 thread_mutex_lock(&mutex);
 for(i=0; i<10000;i++)
  sharei += 1;
printf("Now sharei is %d",sharei);
//给线程解锁
thread_mutex_unlock(&mutex);
}
