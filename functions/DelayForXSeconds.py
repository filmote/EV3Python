#!/usr/bin/env python3
#from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor
import ev3dev2.sensor.lego 
import ev3dev2.led 

from sys import stderr

import threading
import time
import os
import json

def launch(debug, stop, delayLength):

    if debug:
        print("Start delayForXSeconds({}), active number of threads {}, thread {}".format(delayLength, threading.activeCount(), threading.current_thread().ident), file=stderr)

    start_time = time.time()

    while time.time() < start_time + delayLength:

        if stop():
            if debug:
                print("Kill delayForXSeconds({}), thread {}.".format(delayLength, threading.current_thread().ident), file=stderr)
            break

    if not stop():
        if debug:
            print("End delayForXSeconds({}), thread {}.".format(delayLength, threading.current_thread().ident), file=stderr)

