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

void rec(int last, int up, int *dp, int repeat){
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
        } 

        /***********************/
        aux=dp[(i-1)*2+aux_up]+repeat;
        if(aux>=MOD){
            dp[(i-1)*2+aux_up]=mod_abs(aux,MOD);
        }else{
            dp[(i-1)*2+aux_up]=aux;
        }
        /*******/
        
    }
    maior=i;
}

void arcs_for_k_blocks(int k, int *dp, int *new_dp){
    int i,repeat_up,repeat_down;
    int x=maior+1;
    int curr_elem_count=k-2;

    if(x>max_h){
        x=max_h;
    }

    if((max_h=(h-1)*(n-curr_elem_count-1))>limit){
        max_h=limit;
    }
    /*
    printf("k=%d\n",k);
    printf("down\t|\tup\n");
    for(i=0;i<x;i++){
        printf("%d\t|\t%d - i:%d\n",dp[2*i+0],dp[2*i+1],i+1);
    }*/
    for(i=0;i<x;i++){
        if((repeat_down=dp[2*i+0])>0){
            dp[2*i+0]=0; //clean
            rec(i+1,0,new_dp,repeat_down);
            
        }
        if((repeat_up=dp[2*i+1])>0){
            dp[2*i+1]=0; //clean
            rec(i+1,1,new_dp,repeat_up);
        }
       
    }
}

void func(){
    int k;
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
    rec(0,1,dp,1);
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
        //if((max_h=(h-1)*(n/2+n%2)+1-h)>H-h){
        max_h=limit=H-h;
        func();
        printf("%d\n",(int)counter);
    }
}