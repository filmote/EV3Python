#!/usr/bin/env python3
from time import sleep

def printNumber(n):

    print("{}, ".format(n), end="")

    if n < 10:
        printNumber(n + 1)
 
def main():

    printNumber(0)
    print("")
    sleep(5)

if __name__ == '__main__':
    main()