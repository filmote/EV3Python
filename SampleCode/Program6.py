#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C

def onForSeconds(motor, speed, seconds):
    motor.on_for_seconds(speed, seconds, brake = True, block = True)

def main():

    lm1 = LargeMotor(OUTPUT_B)
    lm2 = LargeMotor(OUTPUT_C)
    mm = MediumMotor()
    
    # run these in parallel
    onForSeconds(motor = lm1, speed = 50, seconds = 2)
    onForSeconds(motor = lm2, speed = 40, seconds = 3)

    lm1.wait_until_not_moving()
    lm2.wait_until_not_moving()

    # run this after the previous have completed
    onForSeconds(motor = mm, speed = 10, seconds = 6)

if __name__ == '__main__':
    main()