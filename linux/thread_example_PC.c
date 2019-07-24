#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<semaphore.h>

#define MAXCONUT 10
sem_t sem;
int stack[MAXCOUNT];
int size=0;

void producer(){
 int i;
 for(i=0;i<MAXCOUNT;i++){
 stack[i] = i;
 sem_post(&sem);
 }
}
void consumer(){
 int i;
 while((i=size++)<MAXCOUNT){
 sem_wait(&sem);
 printf("%d X %d = %d", stack[i],stack[i],stack[i]*stack[i]);
 sleep(1);
 }
}
int main()
{
 pthread_t provider, handler;
 sem_init(&sem, 0, 0)
 pthread_create(&provider, NULL, producer, NULL);
 pthread_create(&handler, NULL, consumer, NULL);
 pthread_join(provider, NULL);
 pthread_join(handler, NULL);
 sem_destroy(&sem);
}

