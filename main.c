#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int *slideRight(int board[],int size, int*);
int *slide(int line[],int *non_zeros, int board_size);
int isCandidate(int occ[]);
int isBase2(int);
int *initZeroArray(int size);
int recursiveTries(int* board, int board_size, int max_slide, int slide_count);
int min_slide(int,int,int,int);
void getMinSlide(int *board,int board_size,int max_slide);
int main(void);
/*
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
*/

/**
 * right -> direction=0
 * up    -> direction=1
 * left  -> direction=2
 * down  -> direction=3
*/
int *slideTo(int direction, int* board, int size, int* after_elem_count){
    int elem,non_zeros;
    int *aux,*after_board=(int*)malloc(size*size*sizeof(int));
    after_elem_count=0;
    for(int i=0;i<size;i++){
        aux=initZeroArray(size);
        non_zeros=0;
        if (direction==0) {
            for(int j=0;j<=size;j++){
                elem=board[i*size+j];
                if(elem!=0){
                    aux[non_zeros]=elem;
                    non_zeros++;
                }
            }
        } else if (direction==2) {
            for(int j=size-1; j>-1; j--){
                elem=board[i*size+j];
                if(elem!=0){
                    aux[non_zeros]=elem;
                    non_zeros++;
                }
            }
        } else if (direction==1) {

        } else if (direction==3) {
            
        }
        memcpy(&after_board[i*size],slide(aux,&non_zeros,size),size);
        //after_board[i*size]=slide(aux,&non_zeros,size);
        after_elem_count=after_elem_count+non_zeros;
    }
    return after_board;
}

int *slide(int line[],int *non_zeros, int board_size){
    //returns after_elem_count
    int *final=initZeroArray(board_size);
    int i=*non_zeros-2,i_final=0;
    while(i>=0){
        if(line[i]==line[i+1]){
            final[i_final]= line[i]*2;
            i=i-2;
            *non_zeros--;
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
        arr[i*sizeof(int)]=0; //zero out
    }
    return arr;
}

int recursiveTries(int* board, int board_size, int max_slide, int slide_count){
    //return slide_count
    int elem_count_l,elem_count_r,elem_count_u,elem_count_d;
    int *after_board_l,*after_board_r,*after_board_d,*after_board_u;
    int l,r,d,u;

    if(slide_count<=max_slide){
        //after_board_l=slideLeft(board,board_size,&elem_count_l);
        after_board_r=slideRight(board,board_size,&elem_count_r);
        //after_board_d=slideUp(board,board_size,&elem_count_u);
        //after_board_u=slideDown(board,board_size,&elem_count_d);
        if(elem_count_l==1 || elem_count_r==1 || elem_count_u==1 || elem_count_d==1){
            //free all 4 boards!!! TODO:
            return slide_count;
        }
        else{
            l=recursiveTries(after_board_l,board_size,max_slide,slide_count+1);
            r=recursiveTries(after_board_r,board_size,max_slide,slide_count+1);
            d=recursiveTries(after_board_d,board_size,max_slide,slide_count+1);
            u=recursiveTries(after_board_u,board_size,max_slide,slide_count+1);

            if(r>=0 || l>=0 || d>=0 || u>=0){
                //free all 4 boards!!! TODO:
                return min_slide(l,r,d,u);
            }
            else{
                //free all 4 boards!!! TODO:
                return -1;
            }
        }
    }
    else{
        //free all 4 boards!!! TODO:
        return -1;
    }
        
}

int min_slide(int l, int r, int d,int u){
    int min;
    if(l!=-1){
        min=l;
        if(r!=-1 && r<min){
            min=r;
        }
        if(d!=-1 && d<min){
            min=d;
        }
        if(u!=-1 && u<min){
            min=u;
        }
    }
    else if(r!=-1){
        min=r;
        if(d!=-1 && d<min){
            min=d;
        }
        if(u!=-1 && u<min){
            min=u;
        }
    }
    else if(d!=-1){
        min=d;
        if(u!=-1 && u<min){
            min=u;
        }
    }
    else if(u!=-1){
        min=u;
    }
    return min;
}

void getMinSlide(int *board,int board_size,int max_slide){
    int answer;
    answer= recursiveTries(board,board_size,max_slide,1);
    if(answer==-1)
        printf("no solution\n");
    else
        printf("%d\n",answer);
}

int main(void){
    //read input
    int j,i,num_testcases,board_size,max_slide;
    int *board,*occ;
    int x;

    scanf("%d",&num_testcases);
    for(i=0; i<num_testcases;i++){
        scanf("%d %d",&board_size,&max_slide);
        board=initZeroArray(board_size*board_size);
        occ=initZeroArray(11); //occurrence array
        for(j=0;j<board_size*board_size;j++){
            scanf("%d",&x);
            board[j*sizeof(int)]=x;
            //printf("-> %d\n",*(board+j*sizeof(int)));
            if(x!=0){
                occ[(int)log2(x)]++;
            }
        }
        //neste momento temos board
        //check if board isn't impossible 
        if(isCandidate(occ)){
            getMinSlide(board,board_size,max_slide);
        }
        else{
            printf("no solution\n");
        }
        free(board); free(occ);
    }

    return 0; //end
}