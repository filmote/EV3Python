#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
from collections import namedtuple
import threading

def onForSeconds(motor, speed, seconds):
    motor.on_for_seconds(speed, seconds, brake = True, block = True)

def main():

    actions = []
    Action = namedtuple('Action', 'name, motor, speed, seconds')

    lm1 = LargeMotor(OUTPUT_B)
    lm2 = LargeMotor(OUTPUT_C)
    mm = MediumMotor()
    
    action1 = Action("onForSeconds", lm1, 20, 4)
    action2 = Action("onForSeconds", lm2, 40, 3)
    action3 = Action("onForSeconds", mm, 10, 8)
    actions.append(action1)
    actions.append(action2)
    actions.append(action3)
 
    for action in actions:
        if action.name == "onForSeconds":
            onForSeconds(action.motor, action.speed, action.seconds)

if __name__ == '__main__':
    main()


