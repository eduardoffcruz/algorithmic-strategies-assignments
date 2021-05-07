#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 1000
//max num of vertexs == 1000
int adj_list[MAX][(MAX)*2-1]; //fixed size adj list
int scc[MAX/2][MAX+1];
int low[MAX];
int dfs[MAX]; 
int n; //number of POIs (vertex qnt)
int t; //dfs counter
int scc_counter; //includes subsets with one vertex only (one circuit is made out of 2 vertexes)
int circuit_counter;
int max_scc_vertex_count;
int longest_lane_lenght;
int total_length;

int stack[MAX*2]; //fixed size stack 
int on_stack[MAX];
int stack_counter=0;

void push(int v,int dist){
    stack[stack_counter*2]=v;
    stack[stack_counter*2+1]=dist;
    stack_counter++;
}
int pop(int *dist){
    --stack_counter;
    *dist=stack[stack_counter*2+1];
    return stack[stack_counter*2];
}
/*
int on_stack(int a){
    for(int i=stack_counter-1;i>=0;i--)
        if(stack[i]==a) return 1; //true
    return 0; //false
}*/

int _min(int a, int b){
    if(a<b) return a;
    return b;
}

void print_sccs(){
    int i,j;
    printf("scc counter %d\n",scc_counter);
    for(i=0;i<scc_counter;i++){
        printf("SCC %d\n",i);
        for(j=1;j<=scc[i][0];j++){
            printf("%d ",scc[i][j]);
        }
        printf("\n");
    }
    printf("------\n");
}

void tarjan(int v, int dist){
    int i,w,d,total_scc_len=0;
    int scc_vertex_counter=0;
    low[v-1]=dfs[v-1]=t;
    t++;
    push(v,dist);
    on_stack[v-1]=1;//true
    for(i=1;i<=adj_list[v-1][0];i++){
        w=adj_list[v-1][i*2-1]; //vizinho de V
        //printf("v %d tem como vizinho w %d\n",v,w);
        if(dfs[w-1]==-1){
            tarjan(w,adj_list[v-1][i*2]);
            low[v-1]=_min(low[v-1],low[w-1]);
        }
        else if(on_stack[w-1]){
            low[v-1]=_min(low[v-1],dfs[w-1]);
        }
    }
    if(low[v-1]==dfs[v-1]){
        //printf("v %d é raiz (%d)\n",v,low[v-1]);
        //^se esta condição se verificar v é raiz de uma componente fortemente conexa
        do{
            w=pop(&d);
            on_stack[w-1]=0;//false
            scc[scc_counter][scc_vertex_counter+1]=w;
            scc_vertex_counter++;
            total_scc_len+=d;
        }while(w!=v);
        scc[scc_counter][0]=scc_vertex_counter;
        scc_counter++;
        if(scc_vertex_counter>1){
            //if scc is a circuit (has more that 1 vertexes)
            circuit_counter++;
            total_length+=total_scc_len;
            if(total_scc_len>longest_lane_lenght)
                longest_lane_lenght=total_scc_len;
            if(scc_vertex_counter>max_scc_vertex_count) //para guardar o nr de POIs que o maior SCC tem
                max_scc_vertex_count=scc_vertex_counter;
        }

    }
}

int main(void){
    int test_case_qnt,tc,i;
    int m,q; //m==num of connections between POIs ; q == num of questions asked by the mayor
    int a,b,d,v_count;

    scanf("%d",&test_case_qnt);
    for(tc=0;tc<test_case_qnt;tc++){ //for each test case
        stack_counter=0; //reset top of stack pointer
        scc_counter=0;
        max_scc_vertex_count=0;
        longest_lane_lenght=0;
        total_length=0;
        circuit_counter=0;
        t=1;
        scanf("%d %d %d",&n,&m,&q);
        for(i=0;i<n;i++){
            memset(adj_list[i],0,(n-1)*2*sizeof(int)); //clear adj_list
            low[i]=dfs[i]=-1;
            on_stack[i]=0;
        }
        for(i=0;i<m;i++){
            scanf("%d %d %d",&a,&b,&d);
            v_count=++adj_list[a-1][0];
            adj_list[a-1][v_count*2-1]=b; //vertex b
            adj_list[a-1][v_count*2]=d; //distance from a to b
        }
        for(i=1;i<=n;i++)
            if(dfs[i-1]==-1)
                tarjan(i,0);
        
        //print_sccs();

        switch(q){
            case 1:
                printf("%d\n",circuit_counter);
                break;
            case 2:
                printf("%d %d\n",circuit_counter,max_scc_vertex_count);
                break;
            case 3:
                printf("%d %d %d\n",circuit_counter,max_scc_vertex_count,longest_lane_lenght);
                break;
            case 4:
                printf("%d %d %d %d\n",circuit_counter,max_scc_vertex_count,longest_lane_lenght,total_length);
                break;
        }
    }


    return 0;
}

//slides (Week11 teorica) & slides (Week 1 - Intro to Mooshak and Data Structures)