#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor
from collections import namedtuple
from time import sleep

import threading
import time

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
    Action = namedtuple('Action', 'name, motor, speed, seconds')

    lm1 = LargeMotor(OUTPUT_B)
    lm2 = LargeMotor(OUTPUT_C)
    mm = MediumMotor()
    ts = TouchSensor()
    
    action1 = Action("onForSeconds", lm1, 20, 4)
    action2 = Action("onForSeconds", lm2, 40, 3)
    action3 = Action("delayForSeconds", None, None, 2)
    action4 = Action("onForSeconds", mm, 10, 8)
    
    actionParallel = []
    actionParallel.append(action1)
    actionParallel.append(action2)
    
    actions.append(actionParallel)
    actions.append(action3)
    actions.append(action4)
    
    for action in actions:

        while True:

            # are their multiple actions to execute in parallel?
            if isinstance(action, list):
        
                for subAction in action:
                    thread = launchStep(lambda:stopProcessing, subAction)
                    threadPool.append(thread)
        
            # is there a single action to execute?
            else:
        
                thread = launchStep(lambda:stopProcessing, action)
                threadPool.append(thread)

            # remove any completed threads from the pool
            for thread in threadPool:
                if not thread.isAlive():
                    threadPool.remove(thread)

            # if there are no threads running, exist the 'while' loop 
            # and start the next action from the list 
            if not threadPool:
                break

            # if the touch sensor is pressed, complete everything
            if ts.is_pressed:
                stopProcessing = True
                break

            sleep(0.25)

        # if the 'stopProcessing' flag has been set then break out of the program altogether
        if stopProcessing:
            break

if __name__ == '__main__':
    main()
