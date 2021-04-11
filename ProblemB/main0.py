from sys import stdin,stdout

def readln() -> str: return stdin.readline().rstrip()
def outln(n: int) -> None:  stdout.write(str(n)+'\n')




def rec(h_list,curr_elem_count,up,k,h,max_h):
    #max_h==H-h , valor pode ir de 1 até hi_max inclusivé
    last=h_list[curr_elem_count-1]
    if(curr_elem_count>=k-1): #assures rule 2
        #no more combinations for k elements, add last 0
        if(abs(0-last)>=h): #breaks rule 3
            return False

        #TODO: increment counter!
        print('--->',end='')
        print(h_list)
        return True

    print(h_list)
    for i in range(1,max_h+1):
        aux_up=up
        if(i==last or abs(i-last)>=h): #breaks rule 3
            continue
        elif(up and i<last):
            aux_up=False #descending orden
        elif(not up and i>last): #breaks rule 4
            continue

        h_list[curr_elem_count]=i
        rec(h_list,curr_elem_count+1,aux_up,k,h,max_h)

def arcs_for_k_blocks(k,h,max_h):
    h_list=[0]*k 

    rec(h_list,1,True,k,h,max_h)


def func(n,h,H):
    if(h<=1 or n<3):
        return 0 #impossivel

    max_h=H-h
    for k in range(3,n+1): #k>=3 !!!!!
        arcs_for_k_blocks(k,h,max_h)
    

def main() -> None:

    num_testcases= int(readln())
    for k in range(num_testcases):
        [n, h, H] = [int(parameter) for parameter in readln().split(' ')]
        outln(func(n,h,H))



#board= [[0]*H for i in range(n)]
if __name__=="__main__":
    main()
