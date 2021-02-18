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
        self.board=None
        self.reset(size) #fills size*size board with zeros
                
    def reset(self,size):
        #allocates totally new matrix filled with zeros and assigns it to board
        #previously allocated boards will automatically be freed by python's "garbage collector" 
        self.board=[[0]*size]*size
       




def main():
    """
    #para ler até o EOF
    for line in stdin:
        line=line.rstrip().split(' ')
    """

if __name__=="__main__":
    main()

#pypy3 C.py -m py_compile < test.txt
