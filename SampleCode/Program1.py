#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C

lm1 = LargeMotor(OUTPUT_B)
lm2 = LargeMotor(OUTPUT_C)
mm = MediumMotor()
 
# run these in parallel
lm1.on_for_seconds(speed = 50, seconds=2, brake=True)
lm2.on_for_seconds(speed = 50, seconds=4, brake=True)
 
# run this after the previous have completed
mm.on_for_seconds(speed = 10, seconds=6)
