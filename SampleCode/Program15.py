#!/usr/bin/env python3
from time import sleep

f = open("Program15_data.txt", "r")

for aLineOfText in f:
    print(aLineOfText) 

f.close()
sleep(5)