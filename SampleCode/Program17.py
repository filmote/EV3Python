#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor
from time import sleep

import threading
import time
import types

def onForSeconds(stop, motor, speed, seconds):

    start_time = time.time()
    motor.on(speed, brake = True, block = False)

    while time.time() < start_time + seconds:

        # if we are stopping prematurely break out of loop 
        if stop():
            break

    motor.off()

def delayForSeconds(stop, seconds):

    start_time = time.time()

    while time.time() < start_time + seconds:

        if stop():
            break

def createAction(name, motor, speed, seconds):

    largeMotor_Left = LargeMotor(OUTPUT_B)
    largeMotor_Right = LargeMotor(OUTPUT_C)
    mediumMotor = MediumMotor()

    action = types.SimpleNamespace()
    action.name = name
    action.speed = speed
    action.seconds = seconds

    if (motor == "largeMotor_Left"):
        action.motor = largeMotor_Left
    if (motor == "largeMotor_Right"):
        action.motor = largeMotor_Right
    if (motor == "mm"):
        action.motor = mm

    return action

def launchStep(stop, action):

    if action.name == "onForSeconds":
        thread = threading.Thread(target = onForSeconds, args = (stop, action.motor, action.speed, action.seconds))
        thread.start()
        return thread
    
    if action.name == "delayForSeconds":
        thread = threading.Thread(target = delayForSeconds, args = (stop, action.seconds))
        thread.start()
        return thread

def main():

    threadPool = []
    actions = []
    stopProcessing = False
    
    largeMotor_Left = LargeMotor(OUTPUT_B)
    largeMotor_Right = LargeMotor(OUTPUT_C)
    mediumMotor = MediumMotor()
    ts = TouchSensor()
    
    f = open("Program16_data.txt", "r")

    for aLineOfText in f:

        tokens = aLineOfText .split(",")  

        # read the string values into local variables - make 
        # the speed and seconds floating point numbers
        name = tokens[0]
        motor = tokens[1]
        speed = float(tokens[2])
        seconds = float(tokens[3])

        action = createAction(name, motor, speed, seconds)


        # launch the action
        thread = launchStep(lambda:stopProcessing, action)
        threadPool.append(thread)

        while not stopProcessing:

            # remove any completed threads from the pool
            for thread in threadPool:
                if not thread.isAlive():
                    threadPool.remove(thread)

            # if there are no threads running, exist the 'while' loop 
            # and start the next action from the list 
            if not threadPool:
                break

            # if the touch sensor is pressed then complete everything
            if ts.is_pressed:
                stopProcessing = True

            sleep(0.25)

        # if the 'stopProcessing' flag has been set then break out of the program altogether
        if stopProcessing:
            break


if __name__ == '__main__':
    main()