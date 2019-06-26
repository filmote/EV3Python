#!/usr/bin/env python3
from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from time import sleep
from sys import stderr

cl = ColorSensor()

while True:    # Stop program by pressing any button
    print(cl.raw, file=stderr)


# red (130, 51, 24)
# white 196, 385, 305
#yellow 183, 230, 61
# light blue 79,255, 270