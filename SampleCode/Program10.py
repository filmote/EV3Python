#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
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

    largeMotor_Left = LargeMotor(OUTPUT_B)
    largeMotor_Right = LargeMotor(OUTPUT_C)
    mediumMotor = MediumMotor()
    
    action1 = createAction("onForSeconds", largeMotor_Left, 20, 4)
    action2 = createAction("onForSeconds", largeMotor_Right, 40, 3)
    action3 = createAction("onForSeconds", mediumMotor, 10, 8)
    
    actionParallel = []
    actionParallel.append(action1)
    actionParallel.append(action2)
    
    actions.append(actionParallel)
    actions.append(action3)
    
    for action in actions:

        # are their multiple actions to execute in parallel?
        if isinstance(action, list):
    
            for subAction in action:
                if subAction.name == "onForSeconds":
                    onForSeconds(subAction.motor, subAction.speed, subAction.seconds)
    
        # is there a single action to execute?
        else:
    
            if action.name == "onForSeconds":
                onForSeconds(action.motor, action.speed, action.seconds)


if __name__ == '__main__':
    main()
