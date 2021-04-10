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
    aux= board.copy()
    for height in range(lower_lim, higher_lim): aux[width][height]=1
    return aux

#   Returns True if there's some block
def sameHeights(board:list, width:int, height:int):
    for i in range(width-1, -1, -1):
        if board[i][height-1]==0 and board[i][height]==1: return True
    return False

def generateCombinations(board:list, n:int, h:int, H:int, width:int, lower_lim: int, higher_lim:int, backwarding:bool):
    if lower_lim<0 or higher_lim>=H or n>=H: 
        return 0
    elif width==0: 
        return generateCombinations(buildBlock(board, 0, 0, h), n, h, H, 1, 1, h-1, False)
    elif width==n-1:
        clone_board= buildBlock(board, width, 0, h)
        if board[width-1][h-1]==clone_board[width][h-1]: 
            global combinations_counter
            combinations_counter+= mod_add(combinations_counter, 1, 1000000007)
            return 1
        else: 
            return 0
    else:
        for growing in range(lower_lim, higher_lim+1):
            if not backwarding:
                clone_board= buildBlock(board, width, growing, growing+h)
                result= generateCombinations(clone_board, n, h, H, width+1, growing+1, growing+h, False)
                if result==0: 
                    return generateCombinations(clone_board, n, h, H, width+1, lower_lim-1, higher_lim-1, True)
            else:
                return generateCombinations(clone_board, n, h, H, width+1, growing-h, growing-1, True)
        


#   ========================================================================

def main() -> None:
    num_testcases= int(readln())
    global combinations_counter
    for k in range(num_testcases):
        combinations_counter=0
        [n, h, H] = [int(parameter) for parameter in readln().split(' ')]
        board= [[0]*H for i in range(n)]
        generateCombinations(board, n, h, H, 0, 0, 0, False)
        outln(combinations_counter)
        

if __name__=='__main__': 
    main()



#   test_case1.txt OUTPUT
#   0
#   1
#   2
#   2
#   4
#   5
#   4
#   819

#   test_case2.txt OUTPUT
#   431655757