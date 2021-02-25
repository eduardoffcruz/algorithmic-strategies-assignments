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

def recursive_tries(board,board_size,max_slide,slide_count,hash_table):
    if(slide_count<=max_slide):
        before_elem_count_l,after_elem_count_l,after_board_l=slide_left(board,board_size)
        before_elem_count_r,after_elem_count_r,after_board_r=slide_right(board,board_size)
        before_elem_count_u,after_elem_count_u,after_board_u=slide_up(board,board_size)
        before_elem_count_d,after_elem_count_d,after_board_d=slide_down(board,board_size)
        if(after_elem_count_r==1 or after_elem_count_l==1 or after_elem_count_u==1 or after_elem_count_d==1):
            if(before_elem_count_r==1 or before_elem_count_l==1 or before_elem_count_u==1 or before_elem_count_d==1):
            #para o caso da matrix inicial ter apenas 1 elemento no inicio
                return slide_count-1,hash_table
            else:
                return slide_count,hash_table
        else:
            str_board=str(after_board_l)
            if(str_board in hash_table and slide_count>=hash_table[str_board]):
                l=-1
            else:
                hash_table[str_board]=slide_count
                l,hash_table= recursive_tries(after_board_l,board_size,max_slide,slide_count+1,hash_table)

            str_board=str(after_board_r)
            if(str_board in hash_table and slide_count>=hash_table[str_board]):
                r=-1
            else:
                hash_table[str_board]=slide_count
                r,hash_table=recursive_tries(after_board_r,board_size,max_slide,slide_count+1,hash_table)

            str_board=str(after_board_u)
            if(str_board in hash_table and slide_count>=hash_table[str_board]):
                u=-1
            else:
                hash_table[str_board]=slide_count
                u,hash_table = recursive_tries(after_board_u,board_size,max_slide,slide_count+1,hash_table)

            str_board=str(after_board_d)
            if(str_board in hash_table and slide_count>=hash_table[str_board]):
                d=-1
            else:
                hash_table[str_board]=slide_count
                d,hash_table = recursive_tries(after_board_d,board_size,max_slide,slide_count+1,hash_table)

            if(r>=0 or l>=0 or u>=0 or d>=0):
                #print(" r:{}\n l:{}\n u:{}\n d:{}\n".format(r,l,u,d))
                return  min(i for i in [r,l,u,d] if i>=0),hash_table
            else:
                return -1,hash_table
    else:
        return -1,hash_table


def get_min_slide(board,board_size,max_slide):
    #get value of minimum slides needed to finish the game.
    #if number of slides needed is greater than max_slide, return 'no solution'
    hash_table=dict() #reset
    answer,_ = recursive_tries(board,board_size,max_slide,1,hash_table)
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
