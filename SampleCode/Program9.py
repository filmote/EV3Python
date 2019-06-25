#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
import threading

def onForSeconds(motor, speed, seconds):
    motor.on_for_seconds(speed, seconds, brake = True, block = True)

def createAction(name, motor, speed, seconds):

    action = {}
    action['name'] = name
    action['motor'] = motor
    action['speed'] = speed
    action['seconds'] = seconds

    return action

def main():

    actions = []

    largeMotor_Left = LargeMotor(OUTPUT_B)
    largeMotor_Right = LargeMotor(OUTPUT_C)
    mediumMotor = MediumMotor()
    
    action1 = createAction('onForSeconds', largeMotor_Left, 20, 4)
    action2 = createAction('onForSeconds', largeMotor_Right, 40, 3)
    action3 = createAction('onForSeconds', mediumMotor, 10, 8)
    
    actions.append(action1)
    actions.append(action2)
    actions.append(action3)
 
    for action in actions:
        if action.get('name') == 'onForSeconds':
            onForSeconds(action.get('motor'), action.get('speed'), action.get('seconds')

if __name__ == '__main__':
    main()


