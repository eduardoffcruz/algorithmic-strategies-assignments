from sys import stdin,stdout

def readln() -> str: return stdin.readline().rstrip()
def outln(n: int) -> None:  stdout.write(str(n)+'\n')

#   ========================================================================
combinations_counter= 0
#   modulo 1000000007
def mod_abs(a: int, mod: int): return ((a % mod) + mod) % mod
def mod_add(a: int, b: int, mod: int): return (mod_abs(a, mod) + mod_abs(b, mod)) % mod


def generateCombinations(heights:list, n:int, h:int, H:int, width:int, backwarding:bool):
    #height_lim= H-h
    lower_lim, higher_lim = heights[width-1]+1, heights[width-1]+h
    if width==n-1: 
        if heights[width-1]<=h-1 and heights[width-1]>0:
            global combinations_counter
            combinations_counter= mod_add(combinations_counter, 1, 1000000007)
            outln(heights)
            return
    else:
        for growing in range(lower_lim, higher_lim):
            if heights[width-1]==growing: continue
            if not backwarding:
                if growing > H-h:
                    generateCombinations(heights.copy(), n, h, H, width, True)
                else: 
                    heights[width]= growing
                    generateCombinations(heights.copy(), n, h, H, width+1, False)
            if backwarding:
                if higher_lim-growing<=0: continue
                heights[width]= higher_lim-growing
                generateCombinations(heights.copy(), n, h, H, width+1, True)
            else: continue

def startUpSetup(n:int, h:int, H:int):
    global combinations_counter
    if n<3 or n>=H: outln(combinations_counter)
    else:
        combinations_counter=0
        for k in range(3, n+1):
            heights= [0] * k
            generateCombinations(heights, k, h, H, 1, False)
            print()
        outln(combinations_counter)

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