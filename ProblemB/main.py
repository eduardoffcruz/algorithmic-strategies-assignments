from sys import stdin,stdout

def readln() -> str: return stdin.readline().rstrip()
def outln(n: int) -> None:  stdout.write(str(n)+'\n')

#   ========================================================================
combinations_counter= 0
#   modulo 1000000007
def mod_abs(a: int, mod: int): return ((a % mod) + mod) % mod
def mod_add(a: int, b: int, mod: int): return (mod_abs(a, mod) + mod_abs(b, mod)) % mod
def mod_sub(a: int, b: int, mod: int): return mod_add(a, -b, mod)

def buildBlock(board:list, width:int, lower_lim:int, higher_lim:int):
    aux = [row[:] for row in board]
    for height in range(lower_lim, higher_lim): aux[width][height]=1
    return aux


def generateCombinations(board:list, n:int, h:int, H:int, width:int, lower_lim: int, higher_lim:int, backwarding:bool):
    if lower_lim<=0 or higher_lim>H or n<3 or n>=H: 
        return -1
    elif width==n-1:
        clone_board= buildBlock(board, width, 0, h)
        if board[width-1][h-1]==clone_board[width][h-1]: 
            global combinations_counter
            combinations_counter= mod_add(combinations_counter, 1, 1000000007)
            return 1
        else: 
            return 0
    else:
        if not backwarding:
            for growing in range(lower_lim, higher_lim+1):
                if growing+h>H: 
                    backwarding= True
                    break
                clone_board= buildBlock(board, width, growing, growing+h)
                result= generateCombinations(clone_board, n, h, H, width+1, growing+1, growing+h-1,False)
                if result==0 or result==-1:
                    backwarding= True
                    break
        if backwarding:
            for degrowing in range(higher_lim, lower_lim-2, -1):
                if degrowing-h<0:
                    return
                clone_board= buildBlock(board, width, degrowing-h+1, degrowing+1)
                result= generateCombinations(clone_board, n, h, H, width+1, degrowing-h+1, degrowing, True)
                if result==-1:
                    break
        


#   ========================================================================

def main() -> None:
    num_testcases= int(readln())
    global combinations_counter
    for k in range(num_testcases):
        combinations_counter=0
        [n, h, H] = [int(parameter) for parameter in readln().split(' ')]
        board= [[0]*H for i in range(n)]
        generateCombinations(buildBlock(board, 0, 0, h), n, h, H, 1, 1, h-1, False)
        outln(combinations_counter)
        

if __name__=='__main__': 
    main()



#   test_case1.txt OUTPUT
#   0
#   1
#   2
#   2
#   4
#   54
#   819

#   test_case2.txt OUTPUT
#   431655757