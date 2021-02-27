#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int* slideRight(int** board, int size):
    int board_after[size]; 
    int after_elem_count=0, before_elem_count=0;
    for (int row = 0; row < size; row++) {
        int aux[size], non_zeros=0;
        for (int column = 0; column < size; column++) {
            int elem= board[row][column], i_aux=0;
            if (elem!=0) {
                aux[i_aux++]= elem;
                non_zeros++;
            }
        after_count,board_after[row] = slide(aux, size, non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count
    }
        
    return before_elem_count,after_elem_count,board_after  ;




int isCandidate(int occ[]){
    int count=0,len=11; //2^11=2048
    for(int i=0;i<len;i++){
        count=count+(occ[i]*(int)pow(2,i));
    }
    return isBase2(count);
}
int isBase2(n){
    return (n & (n-1) == 0) && n != 0;
}
int *initArray(int size){
    int i;
    int *arr=(int*)malloc(size*sizeof(int));
    for(i=0;i<size;i++){
        arr+i*sizeof(int)=0 //zero out
    }
    return arr;
}

void getMinSlide(int *board,int board_size){
    int answer;
    answer= recursiveTries();
    if(answer==-1)
        printf("no solution\n");
    else
        printf("%d\n",answer);
}

void main(void){
    //read input
    int row,i,num_testcases,board_size,max_slide;
    int *board,*occ;
    int x;

    scanf("%d",&num_testcases);
    for(i=0; i<num_testcases;i++){
        scanf("%d %d",&board_size,&max_slide);
        board=initArray(board_size*board_size);
        occ=initArray(11); //occurrence array
        for(row=0;row<board_size*board_size;row++){
            scanf("%d",&x);
            (board+row*sizeof(int))=x;
            //printf("-> %d\n",*(board+row*sizeof(int)));
            if(x!=0){
                occ[log2(x)]++;
            }
        }
        //neste momento temos board
        //check if board isn't impossible 
        if(isCandidate(occ)){
            getMinSlide(board,board_size);
        }
        else{
            printf("no solution\n");
        }
        free(board); free(occ);
    }
}