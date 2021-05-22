#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 1000 //max num of vertexs == 1000

struct aresta{
    int v1;
    int v2;
    int dist; //distance between v1---->v2 
};

//tarjan
int adj_list[MAX][MAX]; //fixed size adj list
int scc[MAX][MAX+1]; 
int low[MAX];
int dfs[MAX]; 
//kruskal
int distance[MAX][MAX]; //used for faster minimum spanning tree calculation (this structure is similar to an adjecency matrix but with weights instead of 0s and 1s)
struct aresta arestas[MAX*MAX]; 
int set[MAX], rank[MAX];

//para cada caso de teste:
int n; //number of POIs (vertex qnt)
int t; //dfs counter
int scc_counter; //includes subsets with one vertex only (one circuit is made out of 2 vertexes)
int circuit_counter;
int max_scc_vertex_count;
int longest_lane_lenght;
int total_length;

/*-----fixed size stack---------*/
int stack[MAX], on_stack[MAX];
int stack_counter=0;

void push(int v) { stack[stack_counter++]=v; }
int pop() { return stack[--stack_counter]; }

int min(int a, int b) { return a < b ? a : b; }

/*------------------------------*/

void tarjan(int v) {
    int w, scc_vertex_counter=0;
    
    low[v-1]=dfs[v-1]=t++;

    push(v); 
    on_stack[v-1]=1;   //true
    
    for(int i=1; i <= adj_list[v-1][0]; i++) {
        w= adj_list[v-1][i]; //vizinho de v
        //printf("v %d tem como vizinho w %d\n",v,w);
        if(dfs[w-1]==-1) {
            tarjan(w);
            low[v-1]=min(low[v-1],low[w-1]);
        } 
        // allows to check if vertex is on stack in constant time!
        else if(on_stack[w-1]) low[v-1]= min(low[v-1],dfs[w-1]); //backedge!
    }

    if (low[v-1]==dfs[v-1]) {
        //  se esta condição se verificar v é raiz de uma componente fortemente conexa
        do{
            w= pop();
            on_stack[w-1]= 0;    // false
            scc[scc_counter][scc_vertex_counter+1]= w;
            scc_vertex_counter++;
        } while(w!=v);
        
        scc[scc_counter++][0]= scc_vertex_counter;
        if (scc_vertex_counter>1) {
            //if scc is a circuit (has more that 1 vertexes)
            circuit_counter++;
            //para guardar o nr de POIs (vertexes) que o maior SCC tem
            if(scc_vertex_counter>max_scc_vertex_count) max_scc_vertex_count= scc_vertex_counter;
        }
    }
}

void link(int a, int b) {
    if (rank[a-1]>rank[b-1]) set[b-1]= a;
    else set[a-1]= b;
    
    if (rank[a-1]==rank[b-1]) rank[b-1]++;
}

int find(int v){
    if (set[v-1]!=v) set[v-1]= find(set[v-1]);
    return set[v-1];
}

void _union(int a, int b) { link(find(a),find(b)); }

int compareDist(const void *a1, const void *a2) {
    int d1 = ((struct aresta*)a1)->dist, d2 = ((struct aresta*)a2)->dist;
    return (d1 - d2); //ascending order
}

int calculatemin_lengths_of_scc(int index){
    //1º, para cada scc q seja um circuito ordenamos in ascending order as arestas
    int counter=0;
    int dist,len=0;

    //preencher array com arestas
    for(int i=1; i<=scc[index][0]; i++){
        for(int j=1; j<=scc[index][0]; j++){
            if((dist=distance[scc[index][i]-1][scc[index][j]-1])!=0) { //constant time to acess distance between vertexes
                arestas[counter].v1= scc[index][i]; //v1
                arestas[counter].v2= scc[index][j]; //v2
                arestas[counter++].dist= dist;
            }
        }
        //make set
        set[scc[index][i]-1]= scc[index][i]; 
        rank[scc[index][i]-1]= 0;
    }
    
    //ordenar array com arestas por distancia entre vertices (ascending order (non-descending order))
    qsort(arestas,counter,sizeof(struct aresta),compareDist);

    for(int i=0; i<counter; i++){
        //para cada aresta
        if (find(arestas[i].v1) != find(arestas[i].v2)) {
            len+= arestas[i].dist;
            _union(arestas[i].v1,arestas[i].v2);
        }
    }
    return len;
}

void calculate_all_sccmin_lengths(){
    //precisamos, para cada SCC q seja um circuito já calculado, de obter a minimum spanning tree para cada SCC. Para isso utilizamos o alg de Kruskal
    int i,len;
    for(i=0;i<scc_counter;i++){
        if(scc[i][0]>1){
            //se o SCC tiver mais de 1 POI (vertex) é um circuito
            len= calculatemin_lengths_of_scc(i); //kruskal algorithm call
            total_length+= len;
            if(len>longest_lane_lenght) longest_lane_lenght= len;
        }
    }
}


int main(void){
    int test_case_qnt;
    int m, q;   // m==num of connections between POIs ; q == num of questions asked by the mayor
    int a, b, d, v_count;

    scanf("%d",&test_case_qnt);
    for(int tc=0; tc<test_case_qnt; tc++){ //for each test case
        stack_counter=0; //reset top of stack pointer
        scc_counter=0;
        max_scc_vertex_count=0;
        longest_lane_lenght=0;
        total_length=0;
        circuit_counter=0;
        t=1;
        scanf("%d %d %d",&n,&m,&q);
        for(int i=0; i<n; i++){
            memset(adj_list[i],0,n*sizeof(int)); //clear adj_list
            memset(distance[i],0,n*sizeof(int)); //clear distance matrix
            low[i]=dfs[i]=-1;
            on_stack[i]=0;
        }
        for(int i=0; i<m; i++){
            scanf("%d %d %d",&a,&b,&d);
            v_count=++adj_list[a-1][0];
            adj_list[a-1][v_count]= b; //vertex b
            distance[a-1][b-1]= d;
        }
        for(int i=1;i<=n;i++)
            if(dfs[i-1]==-1) tarjan(i);
        
        if (q==1) printf("%d\n",circuit_counter);
        else if (q==2) printf("%d %d\n",circuit_counter,max_scc_vertex_count);
        else if (q==3 || q==4) {
            calculate_all_sccmin_lengths();
            q==3 ? printf("%d %d %d\n",circuit_counter,max_scc_vertex_count,longest_lane_lenght) : printf("%d %d %d %d\n", circuit_counter, max_scc_vertex_count,longest_lane_lenght, total_length);
        }
    } return 0;
}

//aplicar kruskal algorithm with union-find to find the minimum spanning tree para cada SCC
//slides (Week10 & 11 teorica) & slides (Week 1 - Intro to Mooshak and Data Structures)