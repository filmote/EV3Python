#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
from collections import namedtuple
from time import sleep
import threading

def waitUntilAllThreadsComplete(threadPool): 
    while threadPool:
        for thread in threadPool:
            if not thread.isAlive():
                threadPool.remove(thread)
                    
def onForSeconds(motor, speed, seconds):
    motor.on_for_seconds(speed, seconds, brake = True, block = False)

def delayForSeconds(seconds):
    sleep(seconds)

def launchStep(action):

    if action.name == "onForSeconds":
        thread = threading.Thread(target = onForSeconds, args = (action.motor, action.speed, action.seconds))
        thread.start()
        return thread
    
    if action.name == "delayForSeconds":
        thread = threading.Thread(target = delayForSeconds, args = (action.seconds, ))
        thread.start()
        return thread

def main():

    threadPool = []
    actions = []
    Action = namedtuple('Action', 'name, motor, speed, seconds')

    lm1 = LargeMotor(OUTPUT_B)
    lm2 = LargeMotor(OUTPUT_C)
    mm = MediumMotor()
    
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

        # are their multiple actions to execute in parallel?
        if isinstance(action, list):
    
            for subAction in action:
                thread = launchStep(subAction)
                threadPool.append(thread)
    
        # is there a single action to execute?
        else:
    
            thread = launchStep(action)
            threadPool.append(thread)

        waitUntilAllThreadsComplete(threadPool)

if __name__ == '__main__':
    main()