#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void print_board(int* board[],int size);
int **slideRight(int *board[],int size, int*);
int **slideLeft(int *board[],int size,int *after_elem_count);
int **slideUp(int *board[],int size,int *after_elem_count);
int **slideDown(int *board[],int size,int *after_elem_count);
int *slide(int line[],int *non_zeros, int board_size);
int isCandidate(int occ[]);
int isBase2(int);
int *initZeroArray(int size);
int recursiveTries(int* board[], int board_size, int max_slide, int slide_count,int*);
int min_slide(int,int,int,int);
void getMinSlide(int *board[],int board_size,int max_slide);
void free_board(int *board[],int);
void fill_zeros(int *arr,int);
int main(void);
struct node *search(int *board[],int size);
void insert(int *board[],int slide_count);
int isEqualBoard(int *b1[],int *b2[],int size);

typedef struct node{
    int **board;
    int slide_count;
    struct node* next;
} node;

node *head=NULL;

void insert(int *board[],int slide_count){
    //insert in head
    node* new = (struct node*)malloc(sizeof(node));
    new->board=board;
    new->slide_count=slide_count;
    new->next=head;
    head=new;
}

struct node *search(int *board[],int size){
    node *aux=head;
    while(aux!=NULL){
        if(isEqualBoard(board,aux->board,size)){
            return aux;
        }
        aux=aux->next;
    }
    return NULL;
}

void freeLinkedList(int board_size){
    node *aux=head,*x=aux;
    if(aux!=NULL){
        while(aux->next!=NULL){
            x=aux;
            aux=aux->next;
            free_board(x->board,board_size);
            free(x);
        }
    }
}

int isEqualBoard(int *b1[],int *b2[],int size){
    int i,j;

    for(i=0;i<size;i++){
        for(j=0;j<size;j++){
            if(b1[i][j]!=b2[i][j]){
                return 0;
            }
        }
    }
    return 1;
}



void print_board(int* board[],int size){
    int i,j;
    for(i=0;i<size;i++){
        for(j=0;j<size;j++){
            printf("%d ",board[i][j]);
        }
        printf("\n");
    }
}

void free_board(int *board[],int size){
    int i;
    for(i=0;i<size;i++){
        free(board[i]);
    }
    free(board);
}

int **slideRight(int *board[],int size,int *after_elem_count){
    int i,j,elem,non_zeros;
    int *aux,**after_board;
    after_board=(int **)malloc(size * sizeof(int*));
    for(int i = 0; i <size; i++) after_board[i] = (int *)malloc(size * sizeof(int));
    *after_elem_count=0;
    for(i=0;i<size;i++){
        aux=initZeroArray(size);
        non_zeros=0;
        for(j=0;j<size;j++){
            //elem=board[i*size+j];
            elem=board[i][j]; 
            if(elem!=0){
                aux[non_zeros]=elem;
                non_zeros++;
            }
        }
        after_board[i]=slide(aux,&non_zeros,size);
        //after_board[i*size]=slide(aux,&non_zeros,size);
        *after_elem_count=*after_elem_count+non_zeros;
    }

    return after_board;
}

int **slideLeft(int *board[],int size,int *after_elem_count){
    int i,j,elem,non_zeros;
    int *aux,**after_board;
    after_board=(int **)malloc(size * sizeof(int*));
    for(int i = 0; i <size; i++) after_board[i] = (int *)malloc(size * sizeof(int));
    *after_elem_count=0;
    for(i=0;i<size;i++){
        aux=initZeroArray(size);
        non_zeros=0;
        for(j=size-1;j>=0;j--){
            //elem=board[i*size+j];
            elem=board[i][j]; 
            if(elem!=0){
                aux[non_zeros]=elem;
                non_zeros++;
            }
        }
        after_board[i]=slide(aux,&non_zeros,size);
        //after_board[i*size]=slide(aux,&non_zeros,size);
        *after_elem_count=*after_elem_count+non_zeros;
    }
    return after_board;
}

int **slideDown(int *board[],int size,int *after_elem_count){
    int i,j,elem,non_zeros;
    int *aux,**after_board;
    after_board=(int **)malloc(size * sizeof(int*));
    for(int i = 0; i <size; i++) after_board[i] = (int *)malloc(size * sizeof(int));
    *after_elem_count=0;
    for(i=0;i<size;i++){
        aux=initZeroArray(size);
        non_zeros=0;
        for(j=0;j<size;j++){
            //elem=board[i*size+j];
            elem=board[j][i]; 
            if(elem!=0){
                aux[non_zeros]=elem;
                non_zeros++;
            }
        }
        after_board[i]=slide(aux,&non_zeros,size);
        *after_elem_count=*after_elem_count+non_zeros;
        
    }
    return after_board;
}

int **slideUp(int *board[],int size,int *after_elem_count){
    int i,j,elem,non_zeros;
    int *aux,**after_board;
    after_board=(int **)malloc(size * sizeof(int*));
    for(int i = 0; i <size; i++) after_board[i] = (int *)malloc(size * sizeof(int));
    *after_elem_count=0;
    aux=initZeroArray(size);
    for(i=0;i<size;i++){
        fill_zeros(aux,size);
        non_zeros=0;
        for(j=size-1;j>=0;j--){
            //elem=board[i*size+j];
            elem=board[j][i]; 
            if(elem!=0){
                aux[non_zeros]=elem;
                non_zeros++;
            }
        }
        after_board[i]=slide(aux,&non_zeros,size);
        //after_board[i*size]=slide(aux,&non_zeros,size);
        *after_elem_count=*after_elem_count+non_zeros;
    }
    free(aux);
    return after_board;
}
/*
int *slideLeft(int board[],int size,int *after_elem_count){
    int elem,non_zeros;
    int *aux,*after_board=(int*)malloc(size*size*sizeof(int));
    after_elem_count=0;
    for(int i=0;i<size;i++){
        aux=initZeroArray(size);
        non_zeros=0;
        for(int j=size-1;j>-1;j+){
            elem=board[i*size+j];
            if(elem!=0){
                aux[non_zeros]=elem;
                non_zeros++;
            }
        }
        memcpy(&after_board[i*size],slide(aux,&non_zeros,size),size);
        //after_board[i*size]=slide(aux,&non_zeros,size);
        after_elem_count=after_elem_count+non_zeros;
    }
    return after_board;
}*/
int *slide(int line[],int *non_zeros, int board_size){
    //returns after_elem_count
    int *final=initZeroArray(board_size);
    int i=*non_zeros-2,i_final=0;
    if(*non_zeros==0){
        return final;
    }
    while(i>=0){
        if(line[i]==line[i+1]){
            final[i_final]= line[i]*2;
            i=i-2;
            *non_zeros=*non_zeros-1;
        }
        else{
            final[i_final]= line[i+1];
            if(i==0){
                i_final++;
                final[i_final]=line[i];
                i_final++;
                break;
            }
            i--;
        }
        i_final++;
    }
    //para o caso em que só temos um elemento na lista diferente de 0 OU p.exemplo: [4,4,4]
    if(i==-1) 
        final[i_final]=line[0];
    return final;
}

int isCandidate(int occ[]){
    int count=0,len=11; //2^11=2048
    for(int i=0;i<len;i++){
        count=count+(occ[i]*(int)pow(2,i));
    }
    return isBase2(count);
}
int isBase2(int n){
    return ((n & (n-1)) == 0) && n != 0;
}
int *initZeroArray(int size){
    int i;
    int *arr=(int*)malloc(size*sizeof(int));
    for(i=0;i<size;i++){
        arr[i]=0; //zero out
    }
    return arr;
}
void fill_zeros(int *arr,int size){

    for(int i=0;i<size;i++){
        arr[i]=0; //zero out
    }
}

int recursiveTries(int *board[], int board_size, int max_slide, int slide_count,int *elem_count){
    //return slide_count
    int elem_count_l,elem_count_r,elem_count_u,elem_count_d;
    int **after_board_l,**after_board_r,**after_board_d,**after_board_u;
    int l,r,d,u;
    node* aux;

    if(slide_count<=max_slide){
        if(*elem_count==1){
            return slide_count;
        }
        aux=search(board,board_size);
        if(aux!=NULL){
            if(slide_count>=aux->slide_count){
                return -1;
            }
            else{
                aux->slide_count=slide_count;
                
            }
        }
        else{
            insert(board,slide_count);
        }

        after_board_l=slideLeft(board,board_size,&elem_count_l);
        after_board_r=slideRight(board,board_size,&elem_count_r);
        after_board_u=slideUp(board,board_size,&elem_count_u);
        after_board_d=slideDown(board,board_size,&elem_count_d);


        l=recursiveTries(after_board_l,board_size,max_slide,slide_count+1,&elem_count_l);
        r=recursiveTries(after_board_r,board_size,max_slide,slide_count+1,&elem_count_r);
        d=recursiveTries(after_board_d,board_size,max_slide,slide_count+1,&elem_count_u);
        u=recursiveTries(after_board_u,board_size,max_slide,slide_count+1,&elem_count_d);  
  
        if(r>=0 || l>=0 || d>=0 || u>=0){
            return min_slide(l,r,d,u);
        }
        else{
            //free all 4 boards!!! TODO:
            return -1;
        }      
    }
    else{
        free_board(board,board_size);
        return -1;
    }
        
}

int min_slide(int l, int r, int d,int u){
    int m;
    if(l!=-1){
        m=l;
        if(r!=-1 && r<m){
            m=r;
        }
        if(d!=-1 && d<m){
            m=d;
        }
        if(u!=-1 && u<m){
            m=u;
        }
    }
    else if(r!=-1){
        m=r;
        if(d!=-1 && d<m){
            m=d;
        }
        if(u!=-1 && u<m){
            m=u;
        }
    }
    else if(d!=-1){
        m=d;
        if(u!=-1 && u<m){
            m=u;
        }
    }
    else if(u!=-1){
        m=u;
    }
    else{
        return -1;
    }
    return m;
}

void getMinSlide(int *board[],int board_size,int max_slide){
    int answer,count=0;
    answer = recursiveTries(board,board_size,max_slide,0,&count);
    if(answer==-1)
        printf("no solution\n");
    else
        printf("%d\n",answer);

    freeLinkedList(board_size);
}

int main(void){
    //read input
    int n,j,i,k,num_testcases,board_size,max_slide;
    int **board,*occ;
    int x;

    scanf("%d",&num_testcases);
    for(n=0; n<num_testcases;n++){
        scanf("%d %d",&board_size,&max_slide);
        board= (int **)malloc(board_size * sizeof(int*));
        for(k = 0; k <board_size; k++) board[k] = (int *)malloc(board_size * sizeof(int));
        occ=initZeroArray(11); //occurrence array
        for(i=0;i<board_size;i++){
            for(j=0;j<board_size;j++){
                scanf("%d",&x);
                board[i][j]=x;
                if(x!=0){
                    occ[(int)log2(x)]++;
                }
            }
        }
        //neste momento temos board
        //check if board isn't impossible 
        if(isCandidate(occ)){
            head=NULL;
            getMinSlide(board,board_size,max_slide);
        }
        else{
            printf("no solution\n");
        }
        free_board(board,board_size);
        free(occ);
    }

    return 0; //end
}