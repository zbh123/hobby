#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<semaphore.h>
//编译方法是gcc *.c -o * -w -lpthread
static sem_t A_B, B_C, C_A;

void printA(int n){
 int i=0;
 for(i; i<n; i++){
  sem_wait(&C_A);
  printf("A is %d\n", i);
  sem_post(&A_B);
 }
}
void printB(int n){
 int i=0;
 for(i; i<n; i++){
  sem_wait(&A_B);
  printf("B is %d\n", i);
  sem_post(&B_C);
 }
}
void printC(int n){
 int i=0;
 for(i; i<n; i++){
  sem_wait(&B_C);
  printf("C is %d\n", i);
  sem_post(&C_A);
 }
}

int main(){
 pthread_t A, B, C;
 int n=10;
 sem_init(&A_B, 0, 0);
 sem_init(&B_C, 0, 0);
 sem_init(&C_A, 0, 0);
 pthread_create(&A, NULL, printA, n);
 pthread_create(&B, NULL, printB, n);
 pthread_create(&C, NULL, printC, n);
 pthread_join(A, NULL);
 pthread_join(B, NULL);
 pthread_join(C, NULL);
 sem_destroy(&A_B);
 sem_destroy(&B_C);
 sem_destroy(&C_A);
}


