#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 1000
//max num of vertexs == 1000
int adj_list[MAX][(MAX)*2-1]; //fixed size adj list
int adj_mat[MAX][MAX]; //for minimum spanning tree calculation
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

struct aresta{
    int v1;
    int v2;
    int dist; //weight
};

int stack[MAX]; //fixed size stack 
int on_stack[MAX];
int stack_counter=0;

void push(int v){
    stack[stack_counter++]=v;
}
int pop(){
    return stack[--stack_counter];
}

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

void tarjan(int v){
    int i,w;
    //int total_scc_len=0;
    int scc_vertex_counter=0;
    low[v-1]=dfs[v-1]=t;
    t++;
    push(v);
    on_stack[v-1]=1;//true
    
    for(i=1;i<=adj_list[v-1][0];i++){
        w=adj_list[v-1][i*2-1]; //vizinho de V
        //printf("v %d tem como vizinho w %d\n",v,w);
        if(dfs[w-1]==-1){
            //printf("0->v=%d w=%d dist: %d\n",v,w,adj_list[v-1][i*2]);
            tarjan(w);
            low[v-1]=_min(low[v-1],low[w-1]);
        }
        else if(on_stack[w-1]){
            //backedge!
            low[v-1]=_min(low[v-1],dfs[w-1]);
        }
    }
    if(low[v-1]==dfs[v-1]){
        //printf("v %d é raiz (%d)\n",v,low[v-1]);
        //^se esta condição se verificar v é raiz de uma componente fortemente conexa
        do{
            w=pop();
            on_stack[w-1]=0;//false
            scc[scc_counter][scc_vertex_counter+1]=w;
            scc_vertex_counter++;
            //total_scc_len+=d;
        }while(w!=v);
        scc[scc_counter][0]=scc_vertex_counter;
        scc_counter++;
        if(scc_vertex_counter>1){
            //if scc is a circuit (has more that 1 vertexes)
            circuit_counter++;
            //total_length+=total_scc_len;
            //if(total_scc_len>longest_lane_lenght)
                //longest_lane_lenght=total_scc_len;
            if(scc_vertex_counter>max_scc_vertex_count) //para guardar o nr de POIs que o maior SCC tem
                max_scc_vertex_count=scc_vertex_counter;
        }

    }
}

void link(int a, int b,int* rank, int *set){
    if(rank[a-1]>rank[b-1]){
        set[b-1]=a;
    }
    else{
        set[a-1]=b;
    }
    if(rank[a-1]==rank[b-1]){
        rank[b-1]++;
    }
}

int find(int v, int *set){
    if(set[v-1]!=v){
        set[v-1]=find(set[v-1],set);
    }
    return set[v-1];
}

void _union(int v1, int v2, int *rank, int *set){
    link(find(v1,set),find(v2,set),rank,set);
}

int compareDist(const void *a1, const void *a2) {
    int d1 = ((struct aresta*)a1)->dist;
    int d2 = ((struct aresta*)a2)->dist;
    return (d1 - d2); //ascending order
}

int calculate_min_lengths_of_scc(int index){
    //1º, para cada scc q seja um circuito ordenamos in ascending order as arestas
    //const int max_arestas_qnt=scc[index][0]*scc[index][0];
    //struct aresta arestas[max_arestas_qnt]; 
    struct aresta arestas[MAX]; 
    //int set[scc[index][0]], rank[scc[index][0]];
    int set[MAX], rank[MAX];
    int i,j,counter=0;
    int dist,len=0;
    //printf("check ok1\n");
    //preencher array com arestas
    for(i=1;i<=scc[index][0];i++){
        for(j=1;j<=scc[index][0];j++){
            if((dist=adj_mat[scc[index][i]-1][scc[index][j]-1])!=0){
                arestas[counter].v1=scc[index][i]; //v1
                arestas[counter].v2=scc[index][j]; //v2
                arestas[counter].dist=dist;
                counter++;
                //printf("%d %d\n",scc[index][i],scc[index][j]);
                //printf("%d %d %d\n",arestas[counter].v1,arestas[counter].v2,arestas[counter].dist);
            }

        }

        //make set
        set[scc[index][i]-1]=scc[index][i]; rank[scc[index][i]-1]=0;
    }
    
    //ordenar array com arestas por distancia entre vertices
    qsort(arestas,counter,sizeof(struct aresta),compareDist);

    for(i=0;i<counter;i++){
        //para cada aresta
        //printf("v %d w %d dist %d\n",arestas[i].v1,arestas[i].v2,arestas[i].dist);
        if(find(arestas[i].v1,set)!=find(arestas[i].v2,set)){
            //printf("bateu1\n");
            len+=arestas[i].dist;
            _union(arestas[i].v1,arestas[i].v2,rank,set);
        }
    }

    return len;
}

void calculate_all_scc_min_lengths(){
    //precisamos, para cada SCC q seja um circuito já calculado, de obter a minimum spanning tree para cada SCC. Para isso utilizamos o alg de Kruskal
    int i,len;
    for(i=0;i<scc_counter;i++){
        if(scc[i][0]>1){
            //circuit
            len=calculate_min_lengths_of_scc(i);
            total_length+=len;
            if(len>longest_lane_lenght)
                longest_lane_lenght=len;
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
            memset(adj_mat[i],0,n*sizeof(int)); //clear adj_mat
            low[i]=dfs[i]=-1;
            on_stack[i]=0;
        }
        for(i=0;i<m;i++){
            scanf("%d %d %d",&a,&b,&d);
            v_count=++adj_list[a-1][0];
            adj_list[a-1][v_count*2-1]=b; //vertex b
            adj_list[a-1][v_count*2]=d; //distance from a to b
            adj_mat[a-1][b-1]=d;
        }
        for(i=1;i<=n;i++)
            if(dfs[i-1]==-1)
                tarjan(i);
        
        //print_sccs();

        switch(q){
            case 1:
                printf("%d\n",circuit_counter);
                break;
            case 2:
                printf("%d %d\n",circuit_counter,max_scc_vertex_count);
                break;
            case 3:
                calculate_all_scc_min_lengths();
                printf("%d %d %d\n",circuit_counter,max_scc_vertex_count,longest_lane_lenght);
                break;
            case 4:
                calculate_all_scc_min_lengths();
                printf("%d %d %d %d\n",circuit_counter,max_scc_vertex_count,longest_lane_lenght,total_length);
                break;
        }
    }


    return 0;
}

//aplicar kruskal algorithm with union-find to find the minimum spanning tree para cada SCC
//slides (Week10 & 11 teorica) & slides (Week 1 - Intro to Mooshak and Data Structures)