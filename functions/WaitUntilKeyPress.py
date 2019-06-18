#!/usr/bin/env python3
from ev3dev2.button import Button
from time import sleep
from sys import stderr

import constants
import threading

def launch(debug, stop):

    btn = Button()

    if debug:
        print("Start WaitUntilKeyPress(), active number of threads {}, thread {}".format(threading.activeCount(), threading.current_thread().ident), file=stderr)

    while True:

        if btn.any():   

            if debug:
                print("End WaitUntilKeyPress().".format(threading.current_thread().ident), file=stderr)
            break

        else:
            sleep(0.01)  # Wait 0.01 second

    if stop():
        if debug:
            print("Kill WaitUntilKeyPress().".format(threading.current_thread().ident), file=stderr)
