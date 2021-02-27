#include <stdio.h>
#include <stdlib.h>

int main(void){
    //read input
    int i,j,num_testcases, board_size,max_slide;
    int x;
    int *board;
    scanf("%d",&num_testcases);
    for(i=0; i<num_testcases;i++){
        scanf("%d %d",&board_size,&max_slide);
        board=(int*)malloc(board_size*board_size*sizeof(int*));
        for(j=0;j<board_size*board_size;j++){
            scanf("%d",(board+i*sizeof(int)));
            printf("-> %d\n",*(board+i*sizeof(int)));
        }

        //free(board)
    }
}