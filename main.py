#!/usr/bin/env python3

from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor, ColorSensor
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from time import sleep
from sys import stderr
from ast import literal_eval

import threading
import time
import os
import json
import constants

from utilities import MinimiseJSON
from utilities import RobotLifted
from functions import DriveForXRotations
from functions import DelayForXSeconds
from functions import ReturnWhenObjectWithinXcm
from functions import WaitUntilKeyPress



# --------------------------------------------------------------------------------
#  Launch an individual step.
#
#  Launches an individual step as a new thread. The details of the 'process' node 
#  are queried to determine what step to launch and what parameters are passed.
#  
# 
#  Parameters:      
#
#  debug        - If in debug mode, details will be printed to the console.
#  stop         - Should the process be stopped?
#  action       - JSON process node.  
#
#  Returns:
#  
#  thread       - Reference to the newly created thread. 
#
# --------------------------------------------------------------------------------

def launchStep(debug, stop, action):

    if (action['step'] == 'launchInParallel'):

        # Get all other parameters ..

        delay = action['steps']

        # Create action ..

        thread = threading.Thread(target = launchSteps, args = (debug, stop, action, True))
        thread.start()
        return thread

    # --------------------------------------------------------------------------------

    if (action['step'] == 'launchInSerial'):

        # Get all other parameters ..

        delay = action['steps']

        # Create action ..

        thread = threading.Thread(target = launchSteps, args = (debug, stop, action, False))
        thread.start()
        return thread


    # --------------------------------------------------------------------------------

    if (action['step'] == 'waitUntilKeyPress'):

        # Create action ..

        thread = threading.Thread(target = WaitUntilKeyPress.launch, args = (debug, stop))
        thread.start()
        return thread


    # --------------------------------------------------------------------------------

    if (action['step'] == 'driveForXRotations'):

        # Get all other parameters ..

        rotations = action['rotations']
        speed = action['speed']

        # Create action ..

        thread = threading.Thread(target = DriveForXRotations.launch, args = (debug, stop, rotations, speed))
        thread.start()
        return thread


    # --------------------------------------------------------------------------------

    if (action['step'] == 'delayForXSeconds'):

        # Get all other parameters ..

        delay = action['length']

        # Create action ..

        thread = threading.Thread(target = DelayForXSeconds.launch, args = (debug, stop, delay))
        thread.start()
        return thread


    # --------------------------------------------------------------------------------

    if (action['step'] == 'returnWhenObjectWithinXcm'):

        # Get all other parameters ..

        distance = action['distance']

        # Create action ..

        thread = threading.Thread(target = ReturnWhenObjectWithinXcm.launch, args = (debug, stop, distance))
        thread.start()
        return thread


# --------------------------------------------------------------------------------
#  Launch an set of related steps.
#
#  Launches a set of related steps as individual threads hosted inside a single 
#  thread.  Where actions are nominated to run in parallel, the process continues
#  until all actions are completed.  Where actions are nominated to run serially
#  they are started one after the other.
# 
#  Parameters:      
#
#  debug        - If in debug mode, details will be printed to the console.
#  stop         - Should the process be stopped?
#  actions      - JSON action node or nodes.  
#  inParallel   - Where more than one action is specified, should we launch
#                 the actions in parallel or serial?  Default is in parallel.
#
#  Returns:
#  
#  thread       - Reference to the newly created thread. 
#
# --------------------------------------------------------------------------------
    
def launchSteps(debug, stop, actions, inParallel = True):

    threadPool = []
    stepCount = 0

    stop_threads = False
    

    # Launch the process(es) for this step.  If the step contains sub-steps, then
    # we handle these differently to a single step ..

    if 'steps' in actions:

        if inParallel:
            for process in actions['steps']:
                newThread = launchStep(debug, stop, process)
                threadPool.append(newThread)

        if not inParallel:
            newThread = launchStep(debug, stop, actions['steps'][stepCount])
            stepCount = stepCount + 1
            threadPool.append(newThread)


    # The step is a single action ..

    if 'steps' not in actions:

        newThread = launchStep(debug, stop, actions)
        threadPool.append(newThread)


    allThreadsCompleted = False


    # Query the threads repeatedly to see if any have completed ..

    while not allThreadsCompleted:


        # Loop through the threads and remove finished ones from the thread pool ..

        for worker in threadPool:
            if not worker.isAlive():
                threadPool.remove(worker)


        # If there are no more active threads then check to see if we are done ..

        if not threadPool:


            # If we were running multiple steps in serial and we still have more to go then load the next one ..

            if inParallel == False and stepCount < len(actions['steps']):
                newThread = launchStep(debug, stop, actions['steps'][stepCount])
                threadPool.append(newThread)
                stepCount = stepCount + 1


            # Otherwise we have completed all of the work for this step and we are done ..

            else:
                allThreadsCompleted = True
        
        sleep (0.01) # Give the CPU a rest
        #print("a", file=stderr)



# --------------------------------------------------------------------------------
#  Main routine.
# --------------------------------------------------------------------------------

def main():

    cl = ColorSensor()

    print('Starting Program..', file=stderr)


    # Set up debugging level ..

    debug = constants.DEBUG | constants.DEBUG_THREAD_LIFECYCLE


    # Load JSON and strip out comments ..

    programs = MinimiseJSON.minimise("programs.json")

    
    while True:

        rgb = cl.raw

        for program in programs['programs']:

            rProgram = program['r']
            gProgram = program['g']
            bProgram = program['b']

            #print("compare {} to ({}, {}, {})".format(rgb, rProgram, gProgram, bProgram), file=stderr)

            if abs(rgb[0] - rProgram) < constants.COLOUR_TOLERANCE and abs(rgb[1] - gProgram) < constants.COLOUR_TOLERANCE and abs(rgb[2] - bProgram) < constants.COLOUR_TOLERANCE:

                print("Run {}".format(program["program"]), file = stderr)

                # Load JSON and strip out comments ..

                data = MinimiseJSON.minimise(program['fileName'])


                threadPool = []
                stop_threads = False

                for process in data['steps']:

                    inParallel = False if process['step'] == 'launchInSerial' else True
                    thread = threading.Thread(target = launchSteps, args = (debug, lambda: stop_threads, process, inParallel))
                    threadPool.append(thread)
                    thread.start()

                    allThreadsCompleted = False

                    while not allThreadsCompleted:

                        if RobotLifted.isRobotLifted(debug):
                            stop_threads = True

                        for thread in threadPool:
                            if not thread.isAlive():
                                threadPool.remove(thread)

                        if not threadPool:
                            allThreadsCompleted = True
                        
                        sleep (0.01) # Give the CPU a rest

                    if stop_threads:
                        break
                


    print('Finished.', file = stderr)
    #sleep(15)

if __name__ == '__main__':
    main()