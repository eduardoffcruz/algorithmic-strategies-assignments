from sys import stdin,stdout

def readln(): #read line from stdin
  return stdin.readline().rstrip()

def outln(n): #output line to stdout
  stdout.write(str(n))
  stdout.write("\n")
      
def get_zeros_matrix(size):
    return [([0]*size) for i in range(size)]

def read_board_params():
    line=(readln()).split(' ')
    board_size=int(line[0]) #N
    max_slide=int(line[1]) #M , represents the maximum number of slides allowed
    return board_size,max_slide

def read_board(size):
    board=[]
    for k in range(size):
        board_line=[int(n) for n in (readln()).split(' ')]
        board.append(board_line)
    return board

def print_board(board,size):
    for i in range(size):
            for j in range(size):
                stdout.write(str(board[i][j])+' ')
            stdout.write("\n")

def main():
    num_testcases=int(readln())
    for k in range(num_testcases):
        #for each test case:
        #read test case parameters from stdin
        board_size,max_slide=read_board_params()
        #read board content from stdin
        board=read_board(board_size)
        
        print_board(board,board_size) #só para testar




if __name__=="__main__":
    main()

#pypy3 main.py -m py_compile < test.txt
