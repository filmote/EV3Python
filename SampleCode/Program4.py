#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C

largeMotor_Left = LargeMotor(OUTPUT_B)
largeMotor_Right = LargeMotor(OUTPUT_C)
mediumMotor = MediumMotor()
 
# run these in parallel
largeMotor_Left.on_for_rotations(speed = 30, rotations=4, brake=True, block=False)
largeMotor_Right.on_for_rotations(speed = 40, rotations=3, brake=True, block=False)

largeMotor_Left.wait_until_not_moving()
largeMotor_Right.wait_until_not_moving()

# run this after the previous have completed
mediumMotor.on_for_seconds(speed = 10, seconds=6)
