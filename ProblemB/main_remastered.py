from sys import stdin,stdout

def readln() -> str: return stdin.readline().rstrip()
def outln(n: int) -> None:  stdout.write(str(n)+'\n')

#   ========================================================================
total_combinations_counter, partial_combinations_counter= 0
#   modulo 1000000007
def mod_abs(a: int, mod: int): return ((a % mod) + mod) % mod
def mod_add(a: int, b: int, mod: int): return (mod_abs(a, mod) + mod_abs(b, mod)) % mod


def generateCombinations(heights:list, n:int, h:int, H:int, width:int, backwarding:bool):
    #   lower_lim:  first block of growing
    #   higher_lim:  maximum block of growing
    lower_lim, higher_lim = heights[width-1]+1, heights[width-1]+h
    #   last block
    if width==n-1:
        #   if the height of the previous block is lower than h, there's a connection between the blocks
        if heights[width-1]<h:
            global total_combinations_counter, partial_combinations_counter 
            partial_combinations_counter+=1
            outln(heights)
            return
    else:
        if not backwarding:
            for growing in range(lower_lim, higher_lim):
                if growing > H-h: break
                else: 
                    heights[width]= growing
                    generateCombinations(heights.copy(), n, h, H, width+1, False)
        else:
            for degrowing in range(heights[width-1]-1, heights[width-1]-h+1, -1):
                if degrowing<=0: return
                heights[width]= degrowing-heights[width-1]
                generateCombinations(heights.copy(), n, h, H, width+1, True)

def startUpSetup(n:int, h:int, H:int):
    global total_combinations_counter, partial_combinations_counter
    total_combinations_counter=0
    if n<3 or n>=H: outln(total_combinations_counter)
    else:
        for k in range(3, n+1):
            partial_combinations_counter=0
            heights= [0] * k
            generateCombinations(heights, k, h, H, 1, False)
            total_combinations_counter= mod_add(total_combinations_counter, partial_combinations_counter, 1000000007)
        outln(total_combinations_counter)

#   ========================================================================

if __name__=='__main__': 
    num_testcases= int(readln())
    for k in range(num_testcases):
        [n, h, H] = [int(parameter) for parameter in readln().split(' ')]
        startUpSetup(n, h, H)



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