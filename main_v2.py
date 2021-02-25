from sys import stdin,stdout

#   DEFAULT FUNCS -----------------------------------------

#   READERS -----------------------------------------------
def readln() -> str: return stdin.readline().rstrip()
def readBoardParams():
    line= readln().split(' ')
    board_size=int(line[0]) #N
    max_slide=int(line[1]) #M , represents the maximum number of slides allowed
    return board_size,max_slide

def readBoard(size):
    board=[]
    for k in range(size):
        board_line= [int(n) for n in (readln()).split(' ')]
        board.append(board_line) #append has better performance than concat (+), append uses the same list while concat creates a new instance of a list
    return board

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
    #a new matrix is created so that 'board' remains imaculated
    board_after= [None]*size 
    after_elem_count, before_elem_count = 0, 0
    for row in range(size):
        aux = [None]*size
        non_zeros=0
        for column in range(size):
            if board[row][column]!=0:
                aux[non_zeros]= board[row][column]
                non_zeros+=1
        after_count, aux = slide(aux, size, non_zeros)
        board_after[row]= aux[::-1]
        before_elem_count+=non_zeros
        after_elem_count+=after_count
    return before_elem_count,after_elem_count,board_after    
def slideLeft(board:list, size:int):
    board_after= [None]*size 
    before_elem_count, after_elem_count = 0, 0
    for row in range(size):
        aux = [None]*size
        non_zeros=0
        for column in range(size-1,-1,-1):
            if board[row][column]!=0:
                aux[non_zeros]= board[row][column]
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size, non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count
    return before_elem_count,after_elem_count,board_after
def slideDown(board,size):
    board_after= [None]*size 
    before_elem_count, after_elem_count = 0, 0
    for row in range(size):
        aux = [None]*size
        non_zeros=0
        for column in range(size):
            if board[column][row]!=0:
                aux[non_zeros]= board[column][row]
                non_zeros+=1
        after_count, aux = slide(aux, size, non_zeros)
        board_after[row]= aux[::-1]
        before_elem_count+=non_zeros
        after_elem_count+=after_count
    #transpose matrix
    board_after=[[board_after[column][row] for column in range(size)] for row in range(size)] 
    return before_elem_count,after_elem_count,board_after
def slideUp(board,size):
    board_after= [None]*size 
    before_elem_count, after_elem_count = 0, 0
    for row in range(size):
        aux = [None]*size
        non_zeros=0
        for column in range(size-1,-1,-1):
            if board[column][row]!=0:
                aux[non_zeros]= board[column][row]
                non_zeros+=1
        before_elem_count+=non_zeros
        after_count, board_after[row] = slide(aux, size, non_zeros)
        after_elem_count+=after_count

    #transpose matrix
    board_after = [[board_after[column][row] for column in range(size)] for row in range(size)] 
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

#   RECURSIVITY -------------------------------------------
def recursiveTries(board,board_size,max_slide,slide_count):
    if(slide_count<=max_slide):
        before_elem_count_l,after_elem_count_l,after_board_l = slideLeft(board,board_size)
        before_elem_count_r,after_elem_count_r,after_board_r = slideRight(board,board_size)
        before_elem_count_u,after_elem_count_u,after_board_u = slideUp(board,board_size)
        before_elem_count_d,after_elem_count_d,after_board_d = slideDown(board,board_size)
        if(after_elem_count_r==1 or after_elem_count_l==1 or after_elem_count_u==1 or after_elem_count_d==1):
            #para o caso da matrix inicial ter apenas 1 elemento no inicio
            if before_elem_count_r==1 or before_elem_count_l==1 or before_elem_count_u==1 or before_elem_count_d==1: return slide_count-1
            else: return slide_count
        else:
            if before_elem_count_l==after_elem_count_l and board==after_board_l: l=-1
            else: l= recursiveTries(after_board_l,board_size,max_slide,slide_count+1)

            if before_elem_count_r==after_elem_count_r and board==after_board_r: r=-1
            else: r=recursiveTries(after_board_r,board_size,max_slide,slide_count+1)

            if before_elem_count_u==after_elem_count_u and board==after_board_u: u=-1
            else: u = recursiveTries(after_board_u,board_size,max_slide,slide_count+1)

            if before_elem_count_d==after_elem_count_d and board==after_board_d: d=-1
            else: d = recursiveTries(after_board_d,board_size,max_slide,slide_count+1)

            if r>=0 or l>=0 or u>=0 or d>=0: return  min(i for i in [r,l,u,d] if i>=0)
            else: return -1
    else: return -1
def getMinSlide(board,board_size,max_slide):
    #get value of minimum slides needed to finish the game.
    #if number of slides needed is greater than max_slide, return 'no solution'
    answer = recursiveTries(board,board_size,max_slide,1)
    if answer == -1: return 'no solution'
    else: return str(answer)

def main() -> None:
    num_testcases= int(readln())
    #read test case parameters from stdin
    for k in range(num_testcases):
        board_size, max_slide= readBoardParams()
        #read board content from stdin
        board=readBoard(board_size)

        outln(getMinSlide(board,board_size,max_slide))

if __name__=='__main__': main()

#pypy3 main.py -m py_compile < test.txt
