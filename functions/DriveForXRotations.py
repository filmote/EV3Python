#!/usr/bin/env python3
#from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor, ColorSensor
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from sys import stderr

import threading
import time
import os
import json
import constants

def launch(debug, stop, rotations, speed):

    motorB = LargeMotor(OUTPUT_B)
    tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)

    rotationB = motorB.position

    if debug & constants.DEBUG and debug & constants.DEBUG_THREAD_LIFECYCLE:
        print("Start driveForXRotations({}, {}), active number of threads {}, thread {}".format(rotations, speed, threading.activeCount(), threading.current_thread().ident), file=stderr)
        print("> Starting position {}". format(rotationB), file = stderr)

    tank_pair.on(left_speed=speed, right_speed=speed)

    while motorB.position < rotationB + (rotations * 360):

        if debug & constants.DEBUG and debug & constants.DEBUG_MOVEMENT_ROTATION_CURRENT_POSITION:
            print("> Current position {}". format(motorB.position), file = stderr)

        if stop():
            if debug & constants.DEBUG and debug & constants.DEBUG_THREAD_LIFECYCLE:
                print("Kill driveForXRotations({}, {}), thread {}.".format(rotations, speed, threading.current_thread().ident), file=stderr)
            break

    if not stop():

        print("> Final position {}". format(rotationB), file = stderr)
        tank_pair.off()

        if debug & constants.DEBUG and debug & constants.DEBUG_THREAD_LIFECYCLE:
            print("End driveForXRotations({}, {}), thread {}.".format(rotations, speed, threading.current_thread().ident), file=stderr)
