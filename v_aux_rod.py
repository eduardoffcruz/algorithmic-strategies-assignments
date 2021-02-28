from sys import stdin,stdout
import math

#   READERS -----------------------------------------------
def readln() -> str: return stdin.readline().rstrip()
def readBoardParams():
    line= readln().split(' ')
    board_size=int(line[0]) #N
    max_slide=int(line[1]) #M , represents the maximum number of slides allowed
    return board_size,max_slide

def readBoard(size):
    board=[]
    #flatten_board=[]
    #count=0
    occ=[0]*11 #(log2(2048))
    for k in range(size):
        ln=readln().split(' ')
        board_line=[]
        for n in ln:
            x=int(n)
            board_line.append(x)
            if(x!=0):
                #flatten_board.append(x)
                #count+=1
                occ[int(math.log2(x))]+=1
        board.append(board_line) #append has better performance than concat (+), append uses the same list while concat creates a new instance of a list
    return board,occ #,flatten_board,count #,occ

#   PRINTERS ----------------------------------------------
def outln(n: int) -> None: 
    stdout.write(str(n))
    stdout.write('\n')

def printBoard(board: list, size: int) -> None:
    for i in range(size):
        for j in range(size): 
            stdout.write(str(board[i][j])+' ')
        stdout.write('\n')

#   SLIDERS -----------------------------------------------
def slideRight(board: list, size: int):
    board_after= [[None]*size[0]]*size[1] 
    after_elem_count, before_elem_count = 0, 0
    for row in range(size[0]):
        aux = []
        non_zeros=0
        for column in range(size[1]):
            elem=board[row][column]
            if elem!=0:
                aux.append(elem)
                non_zeros+=1
        after_count,board_after[row] = slide(aux, size[1], non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count
    return before_elem_count,after_elem_count,board_after  
def slideLeft(board:list, size:int):
    board_after= [[None]*size[0]]*size[1]
    before_elem_count, after_elem_count = 0, 0
    for row in range(size[0]):
        aux = []
        non_zeros=0
        for column in range(size[1]-1,-1,-1):
            elem=board[row][column]
            if elem!=0:
                aux.append(elem)
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size[1], non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count
    return before_elem_count,after_elem_count,board_after
def slideDown(board:list,size:int):
    board_after= [[None]*size[0]]*size[1]
    before_elem_count, after_elem_count = 0, 0
    for row in range(size[0]):
        aux = []
        non_zeros=0
        for column in range(size[1]):
            elem=board[column][row]
            if elem!=0:
                aux.append(elem)
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size[0], non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count
    return before_elem_count,after_elem_count,board_after  
def slideUp(board:list,size:int):
    board_after= [[None]*size[0]]*size[1]
    before_elem_count, after_elem_count = 0, 0
    for row in range(size[0]):
        aux = []
        non_zeros=0
        for column in range(size[1]-1,-1,-1):
            elem=board[column][row]
            if elem!=0:
                aux.append(elem)
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size[0], non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count
    return before_elem_count,after_elem_count,board_after
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
  
def getColumn(matrix:list, column:int) -> list: 
    return [row[column] for row in matrix]

#   RECURSIVITY -------------------------------------------
def recursiveTries(board:list, board_size:list, slide_count:int, before_elem:int, after_elem:int, hash_table:dict, max_slide:int):
    if slide_count<=max_slide:
        #para o caso da matrix inicial ter apenas 1 elemento no inicio 
        if after_elem==1: return slide_count
        str_board=str(board)
        if str_board in hash_table and slide_count>=hash_table[str_board]: return -1
        zero_row, zero_column= [0]*board_size[0], [0]*board_size[1]
        if getColumn(board, 0)==zero_column: 
            [row.pop(0) for row in board]
            board_size[1]-=1
        elif getColumn(board, board_size[1]-1)==zero_column: 
            [row.pop(board_size[1]-1) for row in board]
            board_size[1]-=1
        if board[0]==zero_row: 
            board.pop(0)
            board_size[0]-=1
        elif board[board_size[0]-1]==zero_row: 
            board.pop(board_size[0]-1)
            board_size[0]-=1

        hash_table[str_board]=slide_count
        before_elem_count_l,after_elem_count_l,after_board_l = slideLeft(board,board_size)
        before_elem_count_r,after_elem_count_r,after_board_r = slideRight(board,board_size)
        before_elem_count_u,after_elem_count_u,after_board_u = slideUp(board,board_size)
        before_elem_count_d,after_elem_count_d,after_board_d = slideDown(board,board_size)
        
        l = recursiveTries(after_board_l, board_size, slide_count+1, before_elem_count_l, after_elem_count_l, hash_table, max_slide)
        r = recursiveTries(after_board_r, board_size, slide_count+1, before_elem_count_r, after_elem_count_r, hash_table, max_slide)    
        u = recursiveTries(after_board_u, board_size, slide_count+1, before_elem_count_u, after_elem_count_u, hash_table, max_slide)
        d = recursiveTries(after_board_d, board_size, slide_count+1, before_elem_count_d, after_elem_count_d, hash_table, max_slide)
    else: return -1

def getMinSlide(board,board_size,max_slide):
    #get value of minimum slides needed to finish the game.
    #if number of slides needed is greater than max_slide, return 'no solution'
    answer=recursiveTries(board,[16,16],0,0,0,dict(),max_slide)
    if answer == -1: outln('no solution')
    else: outln(answer)


def isCandidate(occ):
    #reduce everything to 2's
    count=0
    for i in range(11):
        count+=occ[i]*2**i
    return isBase2(int(count))
def isBase2(n): return (n & (n-1) == 0) and n != 0

def main() -> None:
    num_testcases= int(readln())
    #read test case parameters from stdin
    for k in range(num_testcases):
        board_size, max_slide= readBoardParams()
        #read board content from stdin
        board,occ=readBoard(board_size)

        #check if board isn't impossible
        if(isCandidate(occ)):
            getMinSlide(board,board_size,max_slide)
        else:
            outln('no solution')

        """
        min_slide_estimate=func(flatten_board,elem_count)
        if(min_slide_estimate!=-1):
            #print('ok {}'.format(min_slide_estimate))
            outln(getMinSlide(board,board_size,min_slide_estimate))
        else:
            outln('no solution')
        """


if __name__=='__main__': main()

#pypy3 main.py -m py_compile < test.txt
