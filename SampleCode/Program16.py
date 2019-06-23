#!/usr/bin/env python3
from time import sleep

f = open("Program16_data.txt", "r")

for aLineOfText in f:

    tokens = aLineOfText .split(",")   
    
    # read the string values into local variables - make 
    # the speed and seconds floating point numbers
    name = tokens[0]
    motor = tokens[1]
    speed = float(tokens[2])
    seconds = float(tokens[3])    

    print( "name = {}, motor = {}, speed = {}, seconds = {}".format(name, motor, speed, seconds) )

f.close()
sleep(5)