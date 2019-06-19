#!/usr/bin/env python3
from ev3dev2.button import Button
from ev3dev2.led import Leds
from time import sleep
from sys import stderr

import constants
import threading

def setLEDColour(colour):

    switcher = {
        0: "RED",
        1: "GREEN",
        2: "YELLOW",
        3: "ORANGE",
        4: "AMBER",
        5: "BLACK",
    }

    colourText = switcher.get(colour, "BLACK")

    leds = Leds()
    leds.set_color('LEFT', colourText) 
    leds.set_color('RIGHT', colourText)
    

def launch(debug, stop, colorSequence = True):

    counter = 0
    colour = 0
    btn = Button()

    if debug:
        print("Start WaitUntilKeyPress(), active number of threads {}, thread {}".format(threading.activeCount(), threading.current_thread().ident), file=stderr)

    while True:

        if colorSequence:

            counter = (counter + 1) % 8
            if (counter == 0):

                colour = (colour + 1) % 5
                setLEDColour(colour)

        if btn.any():   

            leds.all_off()

            if debug:
                print("End WaitUntilKeyPress().".format(threading.current_thread().ident), file=stderr)
            break

        else:
            sleep(0.01)  # Wait 0.01 second

    if stop():

        leds.all_off()
        
        if debug:
            print("Kill WaitUntilKeyPress().".format(threading.current_thread().ident), file=stderr)
