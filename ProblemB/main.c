#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007

int counter;
int n;

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

void rec(int last,int curr_elem_count, int up, int k, int h,int max_h, int *dp, int repeat){
    int lower_bound, upper_bound,i,aux_up;
    unsigned int aux;
    //max_h==H-h , valor pode ir de 1 até hi_max inclusivé
    //last=h_list[curr_elem_count-1]
    if(curr_elem_count>=k-1){
        aux=dp[(last-1)*2+up]+repeat;
        if(aux>=MOD){
            dp[(last-1)*2+up]=mod_abs(aux,MOD);
        }else{
            dp[(last-1)*2+up]=aux;
        }
        //dp[(last-1)*2+up]=mod_add(dp[(last-1)*2+up],repeat,MOD);
        
             
        if(abs(0-last)>=h){
            return;
        }

        aux=counter+repeat;
        if(aux>=MOD){
            counter=mod_abs(aux,MOD);
        }else{
            counter=aux;
        }
        //counter=mod_add(counter,repeat,MOD);
    }
    else{
        if(last-((h-1)*(n-curr_elem_count-1))>=h){ //verifica-se se existe a possibilidade de 'fechar' o arco, se n houver é pq já n existirá solução possível a partir daqui e pdoe descartar-se
            return;
        }
        if(up){
            lower_bound=last-h+1;
            if(lower_bound<1){
                lower_bound=1;
            }
            upper_bound=last+h-1;
            if(upper_bound>max_h){
                upper_bound=max_h;
            }
        }
        else{
            upper_bound=last-1;
            if(upper_bound<1){  //verificar se, para o scenario em q todos os proximos blocos tomam a h=upper_bound, nunca ultrapassam a h=1 antes de formar o arco
                return;
            }
            lower_bound=last-h+1;
            if(lower_bound<1){
                lower_bound=1;
            } 
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
            rec(i,curr_elem_count+1,aux_up,k,h,max_h,dp,repeat);
        }
    } 
}

void arcs_for_k_blocks(int k, int h, int max_h, int*dp, int*new_dp){
    int i,repeat;
    memset(new_dp, 0, max_h*2*sizeof(int)); 
    for(i=0;i<max_h;i++){
        if(dp[2*i+0]>0){
            repeat=dp[2*i+0];
            rec(i+1,k-2,0,k,h,max_h,new_dp,repeat);
        }
        if(dp[2*i+1]>0){
            repeat=dp[2*i+1];
            rec(i+1,k-2,1,k,h,max_h,new_dp,repeat);
        }
    }
    //memcpy(dp,new_dp,max_h*2*sizeof(int));
}

void func(int h, int H){
    int max_h=H-h,k;
    int dp[max_h*2]; //[false,true]
    int new_dp[max_h*2];
    int *pt_aux,*pt_dp=dp,*pt_new_dp=new_dp;
    memset(dp, 0, max_h*2*sizeof(int));

    if(h<=1 || n<3){
        return; //impossivel
    }

    //k>=3 !!!!!
    //calculate for k==3 first to fill dp
    rec(0,1,1,3,h,max_h,dp,1);
    for(k=4;k<=n;k++){
        pt_aux=pt_dp;
        arcs_for_k_blocks(k,h,max_h,pt_dp,pt_new_dp);
        pt_dp=pt_new_dp;
        pt_new_dp=pt_aux;
    }
}    

int main(void){
    int case_tests_qnt,h,H;
    scanf("%d",&case_tests_qnt);
    for(int i=0;i<case_tests_qnt;i++){
        scanf("%d %d %d",&n,&h,&H);
        counter=0;
        func(h,H);
        printf("%d\n",(int)counter);
    }
}