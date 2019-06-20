#!/usr/bin/env python3

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C

ts = TouchSensor()
lm1 = LargeMotor(OUTPUT_B)
lm2 = LargeMotor(OUTPUT_C)
mm = MediumMotor()
 
# run these in parallel
lm1.on_for_rotations(speed = 30, rotations=4, brake=True, block=False)
lm2.on_for_rotations(speed = 40, rotations=3, brake=True, block=False)

# stop the rotations if the user lifts the robot (simulate by pressing the button)
if ts.is_pressed:
  lm1.off()
  lm2.off()

lm1.wait_until_not_moving()
lm2.wait_until_not_moving()

# run this after the previous have completed
mm.on_for_seconds(speed = 10, seconds=6)
