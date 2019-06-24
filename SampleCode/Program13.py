#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor
from time import sleep

import threading
import types

def onForSeconds(motor, speed, seconds):
    motor.on_for_seconds(speed, seconds, brake = True, block = True)

def delayForSeconds(seconds):
    sleep(seconds)

def createAction(name, motor, speed, seconds):

    action = types.SimpleNamespace()
    action.name = name
    action.motor = motor
    action.speed = speed
    action.seconds = seconds

    return action

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
    stopProcessing = False

    largeMotor_Left = LargeMotor(OUTPUT_B)
    largeMotor_Right = LargeMotor(OUTPUT_C)
    mediumMotor = MediumMotor()
    ts = TouchSensor()
    
    action1 = createAction("onForSeconds", largeMotor_Left, 20, 4)
    action2 = createAction("onForSeconds", largeMotor_Right, 40, 3)
    action3 = createAction("delayForSeconds", None, None, 2)
    action4 = createAction("onForSeconds", mediumMotor, 10, 8)
    
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