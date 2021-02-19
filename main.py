from sys import stdin,stdout

def readln(): #read line from stdin
  return stdin.readline().rstrip()

def outln(n): #output line to stdout
  stdout.write(str(n))
  stdout.write("\n")
      
def get_zeros_matrix(size):
    return [([0]*size) for i in range(size)]

def print_board(board,size):
    for i in range(size):
            for j in range(size):
                stdout.write(str(board[i][j])+' ')
            stdout.write("\n")

def main():
    """
    #para ler até o EOF
    for line in stdin:
        line=line.rstrip().split(' ')
    """

if __name__=="__main__":
    main()

#pypy3 C.py -m py_compile < test.txt
