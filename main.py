from sys import stdin,stdout

def readln(): #read line from stdin
  return stdin.readline().rstrip()

def outln(n): #output line to stdout
  stdout.write(str(n))
  stdout.write("\n")

######################################
class GameBoard:
    def __init__(self,size):
        self.size=size
        self.matrix=None
        self.reset(size) #fills size*size board with zeros
                
    def reset(self,size):
        #allocates totally new matrix filled with zeros and assigns it to self.matrix
        #previously allocated matrixes will automatically be freed by python's "garbage collector" 
        self.matrix=[([0]*size) for i in range(size)]
       
    def display(self):
        for i in range(self.size):
            for j in range(self.size):
                stdout.write(str(self.matrix[i][j])+' ')
            stdout.write("\n")




def main():
    board=GameBoard(4)
    board.matrix[1][2]=2
    board.display()
    """
    #para ler até o EOF
    for line in stdin:
        line=line.rstrip().split(' ')
    """

if __name__=="__main__":
    main()

#pypy3 C.py -m py_compile < test.txt
