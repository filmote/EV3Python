#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C

largeMotor_Left = LargeMotor(OUTPUT_B)
largeMotor_Right = LargeMotor(OUTPUT_C)
mediumMotor = MediumMotor()
 
# run these in parallel
largeMotor_Left.on_for_seconds(speed = 50, seconds=2, brake=True)
largeMotor_Right.on_for_seconds(speed = 50, seconds=4, brake=True)
 
# run this after the previous have completed
mediumMotor.on_for_seconds(speed = 10, seconds=6)
