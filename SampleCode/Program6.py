#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C

def onForSeconds(motor, speed, seconds):
    motor.on_for_seconds(speed, seconds, brake = True, block = True)

def main():

    largeMotor_Left = LargeMotor(OUTPUT_B)
    largeMotor_Right = LargeMotor(OUTPUT_C)
    mediumMotor = MediumMotor()
    
    # run these in parallel
    onForSeconds(motor = largeMotor_Left, speed = 50, seconds = 2)
    onForSeconds(motor = largeMotor_Right, speed = 40, seconds = 3)

    largeMotor_Left.wait_until_not_moving()
    largeMotor_Right.wait_until_not_moving()

    # run this after the previous have completed
    onForSeconds(motor = mediumMotor, speed = 10, seconds = 6)

if __name__ == '__main__':
    main()