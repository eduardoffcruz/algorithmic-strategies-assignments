from sys import stdin,stdout
from math import log2

#   READERS -----------------------------------------------
def readln() -> str: return stdin.readline().rstrip()
def readBoardParams():
    line= readln().split(' ')
    board_size=int(line[0]) #N
    max_slide=int(line[1]) #M , represents the maximum number of slides allowed
    return board_size,max_slide

def readBoard(size:int):
    board=[]
    occ=[0]*15
    for k in range(size):
        ln=readln().split(' ')
        board_line=[]
        for n in ln:
            x=int(n)
            board_line.append(x)
            if x!=0:
                occ[int(log2(x))]+=1
        board.append(board_line) #append has better performance than concat (+), append uses the same list while concat creates a new instance of a list
    return board, occ

#   PRINTERS ----------------------------------------------
def outln(n: int) -> None: stdout.write(str(n)+'\n')

last_min_slide=-1

#   SLIDERS -----------------------------------------------
def slideRight(board: list, size: int):
    l,c=0,size
    #a new matrix is created so that 'board' remains imaculated
    board_after= [None]*size 
    after_elem_count = 0
    for row in range(size):
        aux = [None]*size
        non_zeros=0
        for column in range(size):
            elem=board[row][column]
            if elem!=0:
                aux[non_zeros]=elem
                non_zeros+=1  
        after_count,board_after[row] = slide(aux, size, non_zeros)
        after_elem_count+=after_count

        if board_after[row][0]==0: l+=1
        else: l=0
        
        if size-after_count<c: c=size-after_count

    x=min(l,c)
    return after_elem_count,board_after,size-x  

def slideLeft(board:list, size:int):
    l,c=0,size
    board_after= [None]*size 
    after_elem_count = 0
    for row in range(size):
        aux = [None]*size
        non_zeros=0
        for column in range(size-1,-1,-1):
            elem=board[row][column]
            if elem!=0:
                aux[non_zeros]=elem
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size, non_zeros)
        after_elem_count+=after_count
        
        if board_after[row][0]==0: l+=1
        else: l=0

        if size-after_count<c: c=size-after_count

    x=min(l,c)
    return after_elem_count,board_after,size-x

def slideDown(board:list,size:int):
    l,c=0,size
    board_after= [None]*size 
    after_elem_count = 0
    for row in range(size):
        aux = [None]*size
        non_zeros=0
        for column in range(size):
            elem=board[column][row]
            if elem!=0:
                aux[non_zeros]=elem
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size, non_zeros)
        after_elem_count+=after_count

        if board_after[row][0]==0: l+=1
        else: l=0

        if size-after_count<c: c=size-after_count
    
    x=min(l,c)
    #transpose matrix
    return after_elem_count,board_after,size-x
    
def slideUp(board:list,size:int):
    l,c=0,size
    board_after= [None]*size 
    after_elem_count = 0
    for row in range(size):
        aux = [None]*size
        non_zeros=0
        for column in range(size-1,-1,-1):
            elem=board[column][row]
            if elem!=0:
                aux[non_zeros]=elem
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size, non_zeros)

        after_elem_count+=after_count

        if board_after[row][0]==0: l+=1
        else: l=0

        if size-after_count<c: c=size-after_count

    x=min(l,c)
    #transpose matrix
    return after_elem_count,board_after,size-x
 
def slide(orig_row:list, size:int, non_zeros:int):
    # orig_row:   ''compressed'' line e.g: [1,3] instead of [1,0,3,0] 
    # size:  size of original board
    # non_zeros: equal to len(orig_row)
    final= [0]*size
    orig_col, final_col= non_zeros-2, 0
    while orig_col>=0:
        if orig_row[orig_col]==orig_row[orig_col+1]:
            #merge
            final[final_col]= orig_row[orig_col]*2
            orig_col-=2
            non_zeros-=1
        else:
            final[final_col]= orig_row[orig_col+1]
            if orig_col==0:
                final_col+=1
                final[final_col]= orig_row[orig_col]
                final_col+=1
                break
            orig_col-=1
        final_col+=1

    #para o caso em que só temos um elemento na lista diferente de 0 OU p.exemplo: [4,4,4]
    if orig_col==-1: final[final_col]= orig_row[0]
    return non_zeros,final 


#   RECURSIVITY -------------------------------------------
def recursiveTries(board:list,board_size:int,slide_count:int,after_elem:int,hash_table:dict,max_slide:int):
    global last_min_slide
    if slide_count<=max_slide:
        if last_min_slide!=-1 and slide_count>=last_min_slide:
            return -1

        if after_elem==1:
            #para o caso da matrix inicial ter apenas 1 elemento no inicio
            last_min_slide=slide_count 
            return slide_count

        str_board=str(board)
        if str_board in hash_table and slide_count>=hash_table[str_board]:
            return -1
        
        hash_table[str_board]=slide_count
        after_elem_count_d,after_board_d,s_d=slideDown(board,board_size)
        d = recursiveTries(after_board_d,s_d,slide_count+1,after_elem_count_d,hash_table,max_slide) 
        after_elem_count_u,after_board_u,s_u=slideUp(board,board_size)
        u = recursiveTries(after_board_u,s_u,slide_count+1,after_elem_count_u,hash_table,max_slide)
        after_elem_count_r,after_board_r,s_r=slideRight(board,board_size)
        r = recursiveTries(after_board_r,s_r,slide_count+1,after_elem_count_r,hash_table,max_slide) 
        after_elem_count_l,after_board_l,s_l=slideLeft(board,board_size)
        l = recursiveTries(after_board_l,s_l,slide_count+1,after_elem_count_l,hash_table,max_slide)
        
        return _min(r,l,u,d)
        
    else: return -1


def _min(l:int,r:int,d:int,u:int):
    if l!=-1:
        m=l
        if r!=-1 and r<m: m=r
        if d!=-1 and d<m: m=d
        if u!=-1 and u<m: m=u
    elif r!=-1:
        m=r
        if d!=-1 and d<m: m=d
        if u!=-1 and u<m: m=u 
    elif d!=-1:
        m=d
        if u!=-1 and u<m: m=u
    elif u!=-1: m=u
    else: m=-1

    return m

def getMinSlide(board:list,board_size:int,max_slide:int):
    #get value of minimum slides needed to finish the game.
    #if number of slides needed is greater than max_slide, return 'no solution'
    global last_min_slide
    last_min_slide=-1
    answer=recursiveTries(board,board_size,0,0,dict(),max_slide)
    if answer == -1: outln('no solution')
    else: outln(answer)

def isCandidate(occ:list):
    #reduce everything to 2's
    count=0
    for i in range(15): count+=occ[i]*2**i
    return isBase2(int(count))

def isBase2(n:int): return (n & (n-1) == 0) and n != 0

def main() -> None:
    num_testcases= int(readln())
    #read test case parameters from stdin
    for k in range(num_testcases):
        board_size, max_slide= readBoardParams()
        #read board content from stdin
        board,occ=readBoard(board_size)

        #check if board isn't impossible
        if isCandidate(occ): getMinSlide(board,board_size,max_slide)
        else: outln('no solution')

if __name__=='__main__': main()

#pypy3 main.py -m py_compile < test.txt
