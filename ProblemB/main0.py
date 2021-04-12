from sys import stdin,stdout

def readln() -> str: return stdin.readline().rstrip()
def outln(n: int) -> None:  stdout.write(str(n)+'\n')

def mod_abs(a: int, mod: int): return ((a % mod) + mod) % mod
def mod_add(a: int, b: int, mod: int): return (mod_abs(a, mod) + mod_abs(b, mod)) % mod
def mod_sub(a: int, b: int, mod: int): return mod_add(a, -b, mod)


# { k: [[],[],[]] }
def rec(h_list,curr_elem_count,up,k,h,max_h,counter):
    #max_h==H-h , valor pode ir de 1 até hi_max inclusivé
    last=h_list[curr_elem_count-1]
    if(curr_elem_count>=k-1): #assures rule 2
        #no more combinations for k elements, add last 0
        if(abs(0-last)>=h): #breaks rule 3
            return counter
        #print('--->',end='')
        #print(h_list)
        return counter+1

    else:
        #assure rule 3
        if(up):
            lower_bound=last-h+1 #inclusive
            if(lower_bound<1):
                lower_bound=1
            upper_bound=last+h-1 #inclusive
            if(upper_bound>max_h):
                upper_bound=max_h
        else: #assure rule 4
            upper_bound=last-1 #inclusive
            if(upper_bound<1):
                upper_bound=1
            lower_bound=last-h+1 #inclusive
            if(lower_bound<1):
                lower_bound=1

        for i in range(lower_bound,upper_bound+1):
            aux_up=up

            if(i==last): #breaks rule 3
                continue
            elif(up and i<last):
                aux_up=False #descending order

            h_list[curr_elem_count]=i
            counter=rec(h_list,curr_elem_count+1,aux_up,k,h,max_h,counter)

    return counter

def arcs_for_k_blocks(k,h,max_h):
    h_list=[0]*k #[0]*500

    return rec(h_list,1,True,k,h,max_h,0)


def func(n,h,H):
    if(h<=1 or n<3):
        return 0 #impossivel

    max_h=H-h
    counter=0
    for k in range(3,n+1): #k>=3 !!!!!
        counter=mod_add(counter,arcs_for_k_blocks(k,h,max_h),1000000007)
    return counter

def main() -> None:
    num_testcases= int(readln())
    for k in range(num_testcases):
        [n, h, H] = [int(parameter) for parameter in readln().split(' ')]
        outln(func(n,h,H))



#board= [[0]*H for i in range(n)]
if __name__=="__main__":
    main()
