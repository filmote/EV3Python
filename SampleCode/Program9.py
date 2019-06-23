#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
import threading
import types

def onForSeconds(motor, speed, seconds):
    motor.on_for_seconds(speed, seconds, brake = True, block = True)

def createAction(name, motor, speed, seconds):

    action = types.SimpleNamespace()
    action.name = name
    action.motor = motor
    action.speed = speed
    action.seconds = seconds

    return action

def main():

    actions = []

    lm1 = LargeMotor(OUTPUT_B)
    lm2 = LargeMotor(OUTPUT_C)
    mm = MediumMotor()
    
    action1 = createAction("onForSeconds", lm1, 20, 4)
    action2 = createAction("onForSeconds", lm2, 40, 3)
    action3 = createAction("onForSeconds", mm, 10, 8)
    
    actions.append(action1)
    actions.append(action2)
    actions.append(action3)
 
    for action in actions:
        if action.name == "onForSeconds":
            onForSeconds(action.motor, action.speed, action.seconds)

if __name__ == '__main__':
    main()


