from sys import stdin,stdout

#   DEFAULT FUNCS -----------------------------------------
def get_zeros_matrix(size: int): return [[0]*size for i in range(size)]

#   READERS -----------------------------------------------
def readln() -> str: return stdin.readline().rstrip()
def read_board_params():
    line= readln().split(' ')
    board_size=int(line[0]) #N
    max_slide=int(line[1]) #M , represents the maximum number of slides allowed
    if board_size<1 or board_size>20 or max_slide<1 or max_slide>50: return None, None

    return board_size,max_slide

def read_board(size):
    board=[]
    for k in range(size):
        board_line= [int(n) for n in (readln()).split(' ')]
        board.append(board_line)
    return board

#   PRINTERS ----------------------------------------------
def outln(n: int) -> None: stdout.write(str(n)+'\n')
def print_board(board: list, size: int) -> None:
    for i in range(size):
        for j in range(size): 
            for j in range(size):
        for j in range(size): 
            if j!=size-1: stdout.write(str(board[i][j])+' ')
            elif j==size-1 and i!=size-1: stdout.write(str(board[i][j])+'\n')
            else: stdout.write(str(board[i][j])) 

#   SLIDERS -----------------------------------------------
def mergeRow(row: list, direction: str, size: int, actual_pos: int) -> list:
    if direction=='left':
        if row[actual_pos]==row[actual_pos-1]: mergeRow(row, direction, actual_pos-1)
        elif actual_pos==0 or row[actual_pos]!=row[actual_pos-1]: 
            row[actual_pos]*=2
            row[actual_pos+1]=0
    if direction=='right':
        if row[actual_pos]==row[actual_pos+1]: mergeRow(row, direction, actual_pos+1)
        elif actual_pos==size-1 or row[actual_pos]!=row[actual_pos+1]: 
            row[actual_pos]*=2
            row[actual_pos-1]=0
            
def moveRow(row: list, direction: str, size: int, actual_pos: int) -> list:
    if direction=='left':
        if actual_pos==size: return row
        elif row[actual_pos]==0 and actual_pos!=size-1: return moveRow(row, direction, size, actual_pos+1)
        elif row[actual_pos-1]==0: 
            row[actual_pos-1]= row[actual_pos]
            row[actual_pos]=0
            return moveRow(row, direction, size, actual_pos+1)
        elif row[actual_pos-1]!=row[actual_pos]: return moveRow(row, direction, size, actual_pos+1)
        elif row[actual_pos-1]==row[actual_pos]: 
            mergeRow(row, direction, None, actual_pos-1)
            moveRow(row, direction, size, actual_pos-1)
    #   TODO make a right slide row

def slideRow(board: list, size: int, direction: str, slides_counter: int) -> list:
    if size==1: return board
    if direction=='left':
        for row in board: 
            moveRow(row, 'left', size, size-1)
    else:
        for row in board: moveRow(row, 'right', size, 1)
    slides_counter+=1

def main() -> None:
    num_testcases= int(readln())
    for k in range(num_testcases):
        #for each test case:
        #read test case parameters from stdin
        board_size, max_slide= read_board_params()
        if board_size==None: return
        #read board content from stdin
        board=read_board(board_size)
        #   make sure we have a matrix with the defined size
        if len(board)!=board_size or len(board[0])!=board_size: return 
        print_board(board,board_size) #só para testar


if __name__=='__main__': main()

#pypy3 main.py -m py_compile < test.txt
