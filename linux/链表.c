#include<stdio.h>
#include<stdlib.h>
#include<malloc.h>

typedef struct ListNode{
  int value;
  struct ListNode next;
}*PNode;

PNode CreateList(void);
void TraverseList(PNode List);
PNode FindList(PNode List);
void InsertList(PNode List, int pos, int val);
void DeleteList(PNode List, int pos);
void DeleteTheList(PNode List);

int main(){
 PNode List = CreateList();
 TraverseList(List);
 InsertList(List, 3, 100);
 TraverseList(List);
 DeleteList(List, 3);
 TraverseList(List);
 DeleteTheList(List);
}

PNode CreateList(){
 int val. len;
 int i;
 //为链表建立链表头
 PNode PHead = (PNode *)malloc(sizeof(PNode));
 //建立链表尾，让尾等于头并将尾指针指向NULL
 PNode PTail = PHead;
 Ptail->next = NULL;
 printf("Input the number of List");
 scanf("%d", &len);
 for(i=0; i<len;i++){
 printf("The value of %d node",i+1);
 scanf("%d",&val);
 //为指针分配内容
 PNode Temp = (PNode *)malloc(sizeof(PNode));
 Temp->value = val;
 Temp->next = NULL;
 //让尾指针指向Temp
 Ptail->next = Temp;
 //让当前链表的指向下一个链表，便于循环
 Ptail = Temp;
 }
 return PHead;
}
void TraverseList(PNode List){
 int i = 1;
 PNode P = List->next;
 while(P!=NULL){
 printf("the %d node, value is %d\n",i,P->value);
 i++;
 P = P->next;
 }
}
PNode FindList(PNode List){
 PNode P = List->next;
 int val;
 int num = 0;
 printf("Input check value ")
 scanf("%d", val);
 while(P!=NULL && P->value!=val)
 {
 P = P->next;
 ++num;
 }
 if (P==NULL) printf("There has no value %d",val);
 printf("value of %d belong to %d node", val, num+1);
}
void InsertList(PNode List, int pos, int val){
 PNode P = List->next;
 int position=0;
 //遍历链表，获取要找的位置
 while(P!=NULL && position<pos-1){
 P = P->next;
 ++position;
 }
 PNode Temp = (PNode *)malloc(sizeof(PNode));
 Temp->value = val;
 Temp->next = P->next;
 P->next = Temp;
}
void DeleteList(PNode List, int pos){
  PNode P = List->next;
  int position=0;
  while(P!=NUL && position<pos-1){
  P = P->next;
  ++position;
  }
  if(P==NULL) printf("position %d is over index",pos)
  PNode Temp = (PNode *)malloc(sizeof(PNode));
  //将临时链表节点指向下一个节点
  Temp = P->next;
  //让当前节点指向下一个节点的下一个节点
  P->next = Temp->next;
  //释放当前节点的下一个节点
  free(Temp);
  //给释放的节点赋值，防止其成为野指针
  Temp = NULL;
}
void DeleteTheList(PNode List){
 PNode P, Temp;
 P = List->next;
 //防止尾节点不是NULL，或者需要删除整个节点，让尾节点指向NULL
 List->next = NULL;
 //遍历释放节点
 while(P!=NULL){
 Temp = P->next;
 free(P);
 P = Temp;
 }
 printf("Delete ListNode");
}










