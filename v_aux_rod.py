from sys import stdin,stdout
from math import log2
from numpy import count_nonzero
from random import randint

#   READERS -----------------------------------------------
def readln() -> str: return stdin.readline().rstrip()
def readBoardParams():
    line= readln().split(' ')
    size= int(line[0])
    return [size, size], int(line[1])
def readBoard(size: int):
    board=[None]*size
    occ=[0]*11 #(log2(2048))
    for k in range(size):
        ln=readln().split(' ')
        board_line, i_board_line= [None]*size, 0
        for n in ln:
            x=int(n)
            board_line[i_board_line]= x
            i_board_line+=1
            if x!=0: occ[int(log2(x))]+=1
        board[k]= board_line
    return board,occ

#   PRINTERS ----------------------------------------------
def outln(n: int) -> None: 
    stdout.write(str(n))
    stdout.write('\n')
def printBoard(board: list, size: int) -> None:
    for i in range(size[0]):
        for j in range(size[1]): stdout.write(str(board[i][j])+' ')
        stdout.write('\n')

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
    board_after= [[None]*size[1]]*size[0]
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
    board_after= [[None]*size[1]]*size[0]
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
    board_after= [[None]*size[1]]*size[0]
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
    board_after= [[None]*size[1]]*size[0]
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

def getMinSlide(board:list, board_size:list):
    global max_slide
    answer=recursiveTries(board,board_size,0,0,0,dict(),max_slide)
    if answer == -1: return 'no solution'
    else: return str(answer)


def isCandidate(occ):
    #reduce everything to 2's
    count=0
    for i in range(11):
        count+=occ[i]*2**i
    return isBase2(int(count))
def isBase2(n): return (n & (n-1) == 0) and n != 0

def main() -> None:
    global max_slide
    num_testcases= int(readln())
    #read test case parameters from stdin
    for k in range(num_testcases):
        board_size, max_slide= readBoardParams()
        #read board content from stdin
        board,occ= readBoard(board_size[0])
        #check if board isn't impossible
        if isCandidate(occ): outln(getMinSlide(board,board_size))
        else: outln('no solution')

max_slide=0 #global

#   the size must be = 2^x
def generateDoableMatrix(size:int):
    orig_l= [0, 0, 128, 64, 32, 16, 8, 4, 2, 1, 0]
    aux_l= [0, 0, 128, 64, 32, 16, 8, 4, 2, 1, 0]
    max_slide, i_l= 50, 0
    size_matrix= [size, size]
    m = [[0 for col in range(size_matrix[0])] for row in range(size_matrix[0])]

    for row in range(size_matrix[0]):
        for column in range(size_matrix[0]):
            if count_nonzero(aux_l)==0: break
            i_l= randint(0, len(aux_l)-1)
            while aux_l[i_l]==0: i_l= randint(0, len(aux_l)-1)
            m[row][column]= 2**(i_l+1)
            aux_l[i_l]-=1
        if count_nonzero(aux_l)==0: break

    printBoard(m, size_matrix)

if __name__=='__main__': 
    main()
    #test()

#pypy3 main.py -m py_compile < test.txt