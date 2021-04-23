from sys import stdin,stdout

def readln() -> str: return stdin.readline().rstrip()
def outln(n: int) -> None:  stdout.write(str(n)+'\n')

#   ========================================================================
MOD= 1000000007
counter, n, h, max_h, limit, lim_up, lim_down, maior = 0, 0, 0, 0, 0, 0, 0, 0

#   modulo 1000000007
def mod_abs(a: int, mod: int): return ((a % mod) + mod) % mod
def mod_add(a: int, b: int, mod: int): return (mod_abs(a, mod) + mod_abs(b, mod)) % mod

def arcs_for_k_blocks(k, dp, new_dp):
    global counter, n, h, max_h, limit, lim_up, lim_down, maior
    i, index = 0, k-4
    aux, aux1, cum= 0, 0, 0 
    last_max=max_h

    #  para o calc na function rec
    max_h= (h-1)*(n-k+1)
    if max_h > limit: max_h= limit
    if last_max > lim_up: last_max= lim_up
    aux= index+h-1
    if aux > max_h-1: aux= max_h-1

    #  index é a partir de onde começa a contar na dp
    for j in range(index, aux):
        cum= mod_add(cum, dp[i*2+1], MOD)
        new_dp[(i+1)*2+1]= cum 

        if lim_up+(h-2)-(i-index) <= max_h: 
            new_dp[(lim_up+(h-2)-(i-index))*2+1] = cum
        if i+2 < h: counter= mod_add(counter, cum, MOD)
        i+=1
    

    #   lim é o final da dp
    aux=lim_up-1
    if aux > max_h-1: aux = max_h-1
    
    for j in range(i, aux):
        cum=mod_add(cum,mod_add(dp[i*2+1],-dp[(j-(h-1))*2+1],MOD),MOD)
        new_dp[(j+1)*2+1]= cum 
        if j+2 < h: counter= mod_add(counter, cum, MOD)
        i+=1
    
    #   primeiro olhar para os downs na dp e só dps olhar para os ups
    cum= 0
    aux1=lim_down-h+1
    if aux1 < 0: aux1= 0

    for j in range(lim_down, aux1, -1):
        cum= mod_add(cum,dp[j*2],MOD)
        new_dp[(j-1)*2]= cum 
        if j<h: counter=mod_add(counter,cum,MOD)
        i+=1
    
    for j in range(i, 0, -1):
        cum= mod_add(cum,mod_add(dp[j*2],-dp[(j+(h-1))*2],MOD),MOD)
        new_dp[(j-1)*2]= cum
        if j<h: counter=mod_add(counter,cum,MOD)
        i+=1
    
    #   ups to downs
    cum=0
    aux1=last_max-h
    if aux1<0: aux1=0
    
    for j in range(last_max, aux1, -1):
        cum= mod_add(cum,dp[j*2+1],MOD)
        new_dp[(j-1)*2]= mod_add(new_dp[(j-1)*2],cum,MOD) 
        if j<h: counter= mod_add(counter,cum,MOD)
        i+=1
    
    for j in range(i, 0, -1):
        cum= mod_add(cum,mod_add(dp[j*2+1],-dp[(j+(h-1))*2+1],MOD),MOD)
        new_dp[(j-1)*2]= mod_add(new_dp[(j-1)*2],cum,MOD)
        if j<h: counter= mod_add(counter,cum,MOD)
        i+=1
    

    lim_down=last_max-1
    lim_up+=h-1

def func():
    dp= [0]*limit*2 #[false,true]
    new_dp= [0]*limit*2
    
    pt_dp= dp
    pt_new_dp= new_dp

    if h<=1 or n<3: return

    #k>=3 !!!!!
    #calculate for k==3 first to fill dp

    lim_down= 0
    lim_up=h-1
    if lim_up > max_h: lim_up= max_h
    
    for i in range(lim_up): dp[i*2+1]=1  
    counter= lim_up

    for k in range(4, n+1): #   before was n instead of n+1
        pt_aux=pt_dp
        arcs_for_k_blocks(k,pt_dp,pt_new_dp)
        pt_dp= pt_new_dp
        pt_new_dp= pt_aux

#   ========================================================================

if __name__=='__main__': 
    case_tests_qnt, H = 0, 0
    num_testcases= int(readln())
    for k in range(num_testcases):
        [n, h, H] = [int(parameter) for parameter in readln().split(' ')]
        counter=0
        limit= int((h-1)*(n/2+n%2)+1-h)
        max_h=limit
        if max_h > H-h: 
            limit = H-h
            max_h= limit
        func()
        outln(str(counter))



#   test_case1.txt OUTPUT
#   0
#   1
#   2
#   2
#   4
#   54
#   819

#   test_case2.txt OUTPUT
#   431655757