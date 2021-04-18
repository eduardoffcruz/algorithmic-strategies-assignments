#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MOD 1000000007

unsigned long long counter;
int n,h,min_h,max_h;

int mod_abs(unsigned long long a, int mod) {
    return ((a % mod) + mod) % mod;
}
int mod_add(unsigned long long a, unsigned long long b, int mod) {
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

void rec(int last,int curr_elem_count, int up, int k, unsigned long *dp, unsigned long repeat){
    int lower_bound, upper_bound,i,aux_up;
    unsigned long long aux;
    //max_h==H-h , valor pode ir de 1 até hi_max inclusivé
    //last=h_list[curr_elem_count-1]
    if(curr_elem_count>=k-1){
        if(abs(0-last)<h){
            aux=counter+repeat;
            if(aux>=LONG_MAX){
                counter=mod_abs(aux,1000000007);
            }else{
                counter=aux;
            }
            //counter=mod_add(counter,repeat,MOD);
        }
        else if(last-((h-1)*(n-curr_elem_count-1))>=h){ //verifica-se se existe a possibilidade de 'fechar' o arco, se n houver é pq já n existirá solução possível a partir daqui e pdoe descartar-se
            return;
        }
        
        aux=dp[(last-1)*2+up]+repeat;
        if(aux>=LONG_MAX){
            dp[(last-1)*2+up]=mod_abs(aux,1000000007);
        }else{
            dp[(last-1)*2+up]=aux;
        }
        //dp[(last-1)*2+up]=mod_add(dp[(last-1)*2+up],repeat,MOD);
    }
    else{
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
            rec(i,curr_elem_count+1,aux_up,k,dp,repeat);
        }
    } 
}

void arcs_for_k_blocks(int k, unsigned long *dp, unsigned long *new_dp){
    int i;
    unsigned long repeat;
    for(i=0;i<max_h;i++){
        if(dp[2*i+0]>0){
            repeat=dp[2*i+0];
            dp[2*i+0]=0; //clean
            rec(i+1,k-2,0,k,new_dp,repeat);
        }
        if(dp[2*i+1]>0){
            repeat=dp[2*i+1];
            dp[2*i+1]=0; //clean
            rec(i+1,k-2,1,k,new_dp,repeat);
        }
    }
}

void func(){
    int k;
    unsigned long dp[max_h*2]; //[false,true]
    unsigned long new_dp[max_h*2];
    unsigned long *pt_aux,*pt_dp=dp,*pt_new_dp=new_dp;
    memset(dp, 0, max_h*2*sizeof(unsigned long));
    memset(new_dp, 0, max_h*2*sizeof(unsigned long)); 
    
    if(h<=1 || n<3){
        return; //impossivel
    }

    //k>=3 !!!!!
    //calculate for k==3 first to fill dp
    rec(0,1,1,3,dp,1);
    for(k=4;k<=n;k++){
        pt_aux=pt_dp;
        arcs_for_k_blocks(k,pt_dp,pt_new_dp);
        pt_dp=pt_new_dp;
        pt_new_dp=pt_aux;
        counter=mod_abs(counter,1000000007);
    }
}    

int main(void){
    int case_tests_qnt,H;
    scanf("%d",&case_tests_qnt);
    for(int i=0;i<case_tests_qnt;i++){
        scanf("%d %d %d",&n,&h,&H);
        counter=0;
        //calculate max possible height for given n blocks of height h
        if((max_h=(h-1)*(n/2+n%2)+1-h)>H-h){
            max_h=H-h;
        }
        func();
        printf("%d\n",(int)counter);
    }
}