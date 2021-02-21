from sys import stdin,stdout

#   DEFAULT FUNCS -----------------------------------------

#   READERS -----------------------------------------------
def readln() -> str: return stdin.readline().rstrip()
def read_board_params():
    line= readln().split(' ')
    board_size=int(line[0]) #N
    max_slide=int(line[1]) #M , represents the maximum number of slides allowed
    return board_size,max_slide

def read_board(size):
    board=[]
    for k in range(size):
        board_line= [int(n) for n in (readln()).split(' ')]
        board.append(board_line) #append has better performance than concat (+), append uses the same list while concat creates a new instance of a list
    return board

#   PRINTERS ----------------------------------------------
def outln(n: int) -> None: 
    stdout.write(str(n))
    stdout.write('\n')

def print_board(board: list, size: int) -> None:
    for i in range(size):
        for j in range(size): 
            stdout.write(str(board[i][j])+' ')
        stdout.write('\n')
 
#   SLIDERS -----------------------------------------------
#____________RODRIGO
def mergeRow(row: list, direction: str, size: int, actual_pos: int) -> list:
    if direction=='left':
        if actual_pos==0 or row[actual_pos]!=row[actual_pos-1]: 
            row[actual_pos]*=2
            row[actual_pos+1]=0
        elif row[actual_pos]==row[actual_pos-1]: mergeRow(row, direction, actual_pos-1)
    if direction=='right':
        if actual_pos==size-1 or row[actual_pos]!=row[actual_pos+1]: 
            row[actual_pos]*=2
            row[actual_pos-1]=0
        elif row[actual_pos]==row[actual_pos+1]: mergeRow(row, direction, actual_pos+1)
            
def moveRow(row: list, direction: str, size: int, actual_pos: int) -> list:
    if direction=='left':
        if actual_pos==-1: return row
        elif row[actual_pos]==0 and actual_pos!=size-1: return moveRow(row, direction, size, actual_pos+1)
        elif row[actual_pos-1]==0: 
            row[actual_pos-1]= row[actual_pos]
            row[actual_pos]=0
            return moveRow(row, direction, size, actual_pos-1)
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

#____________EDUARDO
#SLIDE RIGHT
def slide_right(board,size):
    #done
    board_after=[]
    after_elem_count=0
    before_elem_count=0
    for i in range(size):
        #"compress" line:
        aux=[]
        count=0 #use counter instead of len() func for optimization purposes
        for j in range(size):
            if(board[i][j]!=0):
                aux.append(board[i][j])
                count+=1
        #
        before_elem_count+=count
        after_count,aux=slide(aux,size,count)
        board_after.append(aux[::-1])
        after_elem_count+=after_count

    return before_elem_count,after_elem_count,board_after

#SLIDE LEFT
def slide_left(board,size):
    #done
    board_after=[] #a new matrix is created so that 'board' remains imaculated
    after_elem_count=0
    before_elem_count=0
    for i in range(size):
        #_________"compress" line:
        aux=[]
        count=0 #use counter instead of len() func for optimization purposes
        for j in range(size-1,-1,-1):
            if(board[i][j]!=0):
                aux.append(board[i][j])
                count+=1
        #_________________________
        before_elem_count+=count
        after_count,aux=slide(aux,size,count)
        board_after.append(aux)
        after_elem_count+=after_count

    return before_elem_count,after_elem_count,board_after

#SLIDE DOWN
def slide_down(board,size):
    #
    board_after=[]
    after_elem_count=0
    before_elem_count=0
    for i in range(size):
        #"compress" line:
        aux=[]
        count=0 #use counter instead of len() func for optimization purposes
        for j in range(size):
            if(board[j][i]!=0):
                aux.append(board[j][i])
                count+=1
        #
        before_elem_count+=count
        after_count,aux=slide(aux,size,count)
        board_after.append(aux[::-1])
        after_elem_count+=after_count

    #transpose matrix
    board_after=[[board_after[j][i] for j in range(size)] for i in range(size)] 

    return before_elem_count,after_elem_count,board_after

#SLIDE UP
def slide_up(board,size):
    #
    board_after=[]
    after_elem_count=0
    before_elem_count=0
    for i in range(size):
        #_________"compress" line:
        count=0 #use counter instead of len() func for optimization purposes
        aux=[]
        for j in range(size-1,-1,-1):
            if(board[j][i]!=0):
                aux.append(board[j][i])
                count+=1
        #_________________________
        before_elem_count+=count
        after_count,aux=slide(aux,size,count)
        board_after.append(aux)
        after_elem_count+=after_count

    #transpose matrix
    board_after=[[board_after[j][i] for j in range(size)] for i in range(size)] 

    return before_elem_count,after_elem_count,board_after
    
def slide(aux,size,count):
    #aux: ''compressed'' line e.g: [1,3] instead of [1,0,3,0] 
    #size: size of original board
    #count: equal to len(aux)
    final=[]

    j=count-2
    while(j>=0):
        if(aux[j]==aux[j+1]):
            #merge
            final.append(aux[j]*2)
            j-=2
            count-=1
        else:
            final.append(aux[j+1])
            if(j==0):
                final.append(aux[j])
                break
            j-=1
    if(j==-1):
        #para o caso em que só temos um elemento na lista diferente de 0 OU p.exemplo: [4,4,4]
        final.append(aux[0])
    final.extend([0]*(size-count)) #fill with zeros
    return count,final 

def recursive_tries(board,board_size,max_slide,slide_count):
    if(slide_count<=max_slide):
        before_elem_count_l,after_elem_count_l,after_board_l=slide_left(board,board_size)
        before_elem_count_r,after_elem_count_r,after_board_r=slide_right(board,board_size)
        before_elem_count_u,after_elem_count_u,after_board_u=slide_up(board,board_size)
        before_elem_count_d,after_elem_count_d,after_board_d=slide_down(board,board_size)
        if(after_elem_count_r==1 or after_elem_count_l==1 or after_elem_count_u==1 or after_elem_count_d==1):
            if(before_elem_count_r==1 or before_elem_count_l==1 or before_elem_count_u==1 or before_elem_count_d==1):
            #para o caso da matrix inicial ter apenas 1 elemento no inicio
                return slide_count-1
            else:
                return slide_count
        else:
            if(before_elem_count_l==after_elem_count_l and board==after_board_l):
                l=-1
            else:
                l= recursive_tries(after_board_l,board_size,max_slide,slide_count+1)

            if(before_elem_count_r==after_elem_count_r and board==after_board_r):
                r=-1
            else:
                r=recursive_tries(after_board_r,board_size,max_slide,slide_count+1)

            if(before_elem_count_u==after_elem_count_u and board==after_board_u):
                u=-1
            else:
                u = recursive_tries(after_board_u,board_size,max_slide,slide_count+1)

            if(before_elem_count_d==after_elem_count_d and board==after_board_d):
                d=-1
            else:
                d = recursive_tries(after_board_d,board_size,max_slide,slide_count+1)

            if(r>=0 or l>=0 or u>=0 or d>=0):
                return  min(i for i in [r,l,u,d] if i>=0)
            else:
                return -1
    else:
        return -1


def get_min_slide(board,board_size,max_slide):
    #get value of minimum slides needed to finish the game.
    #if number of slides needed is greater than max_slide, return 'no solution'
    answer = recursive_tries(board,board_size,max_slide,1)
    if(answer == -1):
        return 'no solution'
    else:
        return str(answer)


def main() -> None:
    num_testcases= int(readln())
    for k in range(num_testcases):
        #for each test case:
        #read test case parameters from stdin
        board_size, max_slide= read_board_params()
        #read board content from stdin
        board=read_board(board_size)

        outln(get_min_slide(board,board_size,max_slide))



if __name__=='__main__': main()

#pypy3 main.py -m py_compile < test.txt
