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
        
    return before_elem_count,after_elem_count,board_after  

int isCandidate(int *occ){
    int len=11; //2^11=2048


}

int isBase2(n){
    return (n & (n-1) == 0) && n != 0;
}

int *intArray()


int main(void){
    //read input
    int row,i,num_testcases,board_size,max_slide;
    int *board,*occ;
    int x;


    scanf("%d",&num_testcases);
    for(i=0; i<num_testcases;i++){
        scanf("%d %d",&board_size,&max_slide);
        board=(int*)malloc(board_size*board_size*sizeof(int));
        occ=(int*)malloc(11*sizeof(int)); //occurrence array
        for(row=0;row<board_size*board_size;row++){
            scanf("%d",&x);
            (board+row*sizeof(int))=x
            //printf("-> %d\n",*(board+row*sizeof(int)));
            if(x!=0){
                if(occ[log2(x)])
                occ[log2(x)]+=1
            }
        }
        //neste momento temos board

        //free(board)
    }
}