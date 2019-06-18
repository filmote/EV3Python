#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor
import ev3dev2.sensor.lego 
import ev3dev2.led 
import constants

from sys import stderr

import threading
import time
import os
import json

def launch(debug, stop, distance):

    ir = InfraredSensor() 

    if debug:
        print("Start returnWhenObjectWithinXcm({}), active number of threads {}, thread {}".format(distance, threading.activeCount(), threading.current_thread().ident), file=stderr)

    while True:

        if debug:
            #print(ir.proximity / constants.IR_PROMIXITY_TO_CM_RATIO, file = stderr)
            pass

        if ir.proximity < distance * constants.IR_PROMIXITY_TO_CM_RATIO:
            if debug:
                print("End returnWhenObjectWithinXcm({}).".format(distance, threading.current_thread().ident), file=stderr)
            break

        if stop():
            if debug:
                print("Kill returnWhenObjectWithinXcm({}).".format(distance, threading.current_thread().ident), file=stderr)
            break