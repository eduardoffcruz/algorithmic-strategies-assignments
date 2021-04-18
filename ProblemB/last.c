#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007

int counter;
int n,h,max_h,limit;
int maior;

int mod_abs(int a, int mod) {
    return ((a % mod) + mod) % mod;
}
int mod_add(int a, int b, int mod) {
    return (mod_abs(a, mod) + mod_abs(b, mod)) % mod;
}

void print_dp(int *dp, int s){
    int i,j;
    for(i=0;i<s;i++){
        printf("%d -> ",i+1);
        for(j=0;j<2;j++){
            if(j==0){
                printf("False:");
            }else{printf("True:");}
            printf("%d ",dp[i*2+j]);
        }
        printf("\n");
    }
}
/*
void rec(int last, int up, int *dp, int repeat, int *miss){
    int lower_bound, upper_bound,i,aux_up;
    unsigned int aux;
    //max_h==H-h , valor pode ir de 1 até hi_max inclusivé
    //last=h_list[curr_elem_count-1]
    lower_bound=last-h+1;
    if(lower_bound<1){
        lower_bound=1;
    }
    upper_bound=last+up*h-1;
    if(upper_bound>max_h){
        upper_bound=max_h;
    }
    for(i=lower_bound;i<=upper_bound;i++){
        aux_up=up;
        if(i==last){
            continue;
        }
        else if(up && i<last){
            //DOWN
            aux_up=0;
        }
        
        if(i<h){
            aux=counter+repeat;
            if(aux>=MOD){
                counter=mod_abs(aux,MOD);
            }else{
                counter=aux;
            }

            miss[i-1]=0;
        } 
        else{
            miss[i-1]+=1;
        }
   
        aux=dp[(i-1)*2+aux_up]+repeat;
        if(aux>=MOD){
            dp[(i-1)*2+aux_up]=mod_abs(aux,MOD);
        }else{
            dp[(i-1)*2+aux_up]=aux;
        }
     
        
    }
    maior=i;
}
*/
void arcs_for_k_blocks(int k, int *dp, int *new_dp){
    int i,j,repeat_up,repeat_down;
    int x=maior+1;

    int index=k-4,lim=index+(h-1)+(h-2)*index;
    int aux=0,cum=0;
    //dp[0]=1;dp[1]=3;dp[2]=6,dp[3]=7,dp[4]=6,dp[5]=3,dp[6]=1;
    //UP
    if(x>max_h){
        x=max_h;
    }
    if((max_h=(h-1)*(n-k+1))>limit){
        max_h=limit;
    }

    
    printf("k:%d index %d lim:%d\n",k,index,lim);
    for(i=index;i<lim;i++){
        printf("%d ",dp[i]);
    }printf("\n");

    for(i=index;i<index+h-1;i++){
        cum+=dp[i];
        new_dp[i+1]=cum; 
        new_dp[(lim+(h-2)-(i-index))]=cum;
        //printf("i:%d | i:%d\n",i+1,(lim+(h-2)-(i-index)));
    }
    for(i=i;i<lim-1;i++){
        //printf("cum: %d+%d-%d | i:%d\n",cum,dp[i],dp[i-(h-1)],i);
        cum+=dp[i]-dp[i-(h-1)];
        new_dp[i+1]=cum; 
    }
    
    for(i=index+1;i<lim+(h-1);i++){
        printf("%d ",new_dp[i]);
    }printf("\n");


/*
[1,3,6,7,6,3,1]
 +[1,3,6,7,6,3,1]
   +[1,3,6,7,6,3,1]
        =
[1,4,10,16,19,16,10,4,1]
*/

/*

*/

    /*
    printf("k=%d\n",k);
    printf("down\t|\tup\n");
    for(i=0;i<x;i++){
        printf("%d\t|\t%d - i:%d\n",dp[2*i+0],dp[2*i+1],i+1);
    }
    for(i=0;i<x;i++){
        if((repeat_down=dp[2*i+0])>0){
            dp[2*i+0]=0; //clean
            rec(i+1,curr_elem_count,0,k,new_dp,repeat_down,miss);
            
        }
        if( (repeat_up=dp[2*i+1])>0){
            dp[2*i+1]=0; //clean
            rec(i+1,curr_elem_count,1,k,new_dp,repeat_up,miss);
        }
       
    }*/

}

void func(){
    int k,i,lim;
    int dp[max_h*2]; //[false,true]
    int new_dp[max_h*2];
    int *pt_aux,*pt_dp=dp,*pt_new_dp=new_dp;
    memset(dp, 0, max_h*2*sizeof(int));
    memset(new_dp, 0, max_h*2*sizeof(int)); 
    
    if(h<=1 || n<3){
        return; //impossivel
    }

    //k>=3 !!!!!
    //calculate for k==3 first to fill dp
    //rec(0,1,1,3,dp,1,miss);

    //init set k=3
    if((lim=h-1)>max_h){
        lim=max_h;
    }
    for(i=1;i<=lim;i++){
        dp[i-1]=1;
    }maior=lim;

    for(k=4;k<=n;k++){
        pt_aux=pt_dp;
        arcs_for_k_blocks(k,pt_dp,pt_new_dp);
        pt_dp=pt_new_dp;
        pt_new_dp=pt_aux;
    }

    /*
    printf("----\n"); 
        for(i=0;i<limit;i++){
        if(miss[i]!=0){
            printf("k = %d | missed height %d , %d times\n",k-1,i+1,miss[i]);
        }
        }*/
}    

int main(void){
    int case_tests_qnt,H;
    scanf("%d",&case_tests_qnt);
    for(int i=0;i<case_tests_qnt;i++){
        scanf("%d %d %d",&n,&h,&H);
        counter=0;
        //calculate max possible height for given n blocks of height h
        max_h=limit=H-h;
        func();
        printf("%d\n",(int)counter);
    }
}