from sys import stdin,stdout
from math import log2

def readln() -> str: return stdin.readline().rstrip()
def outln(n: int) -> None:  stdout.write(str(n)+'\n')

#   ========================================================================
def mod_abs(a: int, mod: int): return ((a % mod) + mod) % mod

def mod_add(a: int, b: int, mod: int): return (mod_abs(a, mod) + mod_abs(b, mod)) % mod

def mod_sub(a: int, b: int, mod: int): return mod_add(a, -b, mod)



#   ========================================================================

def main() -> None:
    num_testcases= int(readln())
    #read test case parameters from stdin
    for k in range(num_testcases):
        [n, h, H] = [int(parameter) for parameter in readln().split(' ')]
        


if __name__=='__main__': main()




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