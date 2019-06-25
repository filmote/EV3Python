#!/usr/bin/env python3

def createAction(name, motor, speed, seconds):

    largeMotor_Left = LargeMotor(OUTPUT_B)
    largeMotor_Right = LargeMotor(OUTPUT_C)
    mediumMotor = MediumMotor()

    action = {}
    action['name'] = name
    action['speed'] = speed
    action['seconds'] = seconds

    if (motor == "largeMotor_Left"):
        action['motor'] = largeMotor_Left
    if (motor == "largeMotor_Right"):
        action['motor'] = largeMotor_Right
    if (motor == "mediumMotor"):
        action['motor'] = mediumMotor

    return action


def main():
    action = createAction('sdfsd', 34, 56, 'dd')
    print(action)

if __name__ == '__main__':
    main()