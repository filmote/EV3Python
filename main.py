#!/usr/bin/env python3

from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor, ColorSensor
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from time import sleep
from sys import stderr

import threading
import time
import os
import json
import constants

from functions import DriveForXRotations
from functions import DelayForXSeconds
from functions import ReturnWhenObjectWithinXcm



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
    threadPoolTotalCount = 0
    threadPoolCount = 0
    stepCount = 0

    stop_threads = False
    

    # Launch the process(es) for this step.  If the step contains sub-steps, then
    # we handle these differently to a single step ..

    if 'steps' in actions:

        if inParallel:
            for process in actions['steps']:
                newThread = launchStep(debug, stop, process)
                threadPool.append(newThread)
                threadPoolCount = threadPoolCount + 1

        if not inParallel:
            newThread = launchStep(debug, stop, actions['steps'][stepCount])
            stepCount = stepCount + 1
            threadPool.append(newThread)
            threadPoolCount = threadPoolCount + 1


    # The step is a single action ..

    if 'steps' not in actions:

        newThread = launchStep(debug, stop, actions)
        threadPool.append(newThread)
        threadPoolCount = 1


    threadPoolTotalCount = threadPoolCount
    allThreadsCompleted = False


    # Query the threads repeatedly to see if any have completed ..

    while not allThreadsCompleted:


        # Loop through the threads and remove finished ones from the thread pool ..

        for worker in threadPool:
            if not worker.isAlive():
                threadPool.remove(worker)
                threadPoolCount = threadPoolCount - 1


        # If there are no more active threads then check to see if we are done ..

        if not threadPool:


            # If we were running multiple steps in serial and we still have more to go then load the next one ..

            if inParallel == False and stepCount < len(actions['steps']):
                newThread = launchStep(debug, stop, actions['steps'][stepCount])
                threadPool.append(newThread)
                stepCount = stepCount + 1
                threadPoolCount = threadPoolCount + 1


            # Otherwise we have completed all of the work for this step and we are done ..

            else:
                allThreadsCompleted = True
        
        sleep (0.01) # Give the CPU a rest
        #print("a", file=stderr)


# --------------------------------------------------------------------------------
#  Has the robot been lifted off the table?
# 
#  Parameters:      
#
#  debug        - If in debug mode, details will be printed to the console.
#                 the actions in parallel or serial?  Default is in parallel.
#
#  Returns:
#  
#  boolean      - True if the robot has been lifted off the table.
#               - False if the robot is still on the table.
#
# --------------------------------------------------------------------------------

def isRobotLifted(debug):

    MINIMUM_THRESHOLD = 10
    cl = ColorSensor() 
    # print(cl.raw, file = stderr)
    lifted = cl.raw[0] < MINIMUM_THRESHOLD and cl.raw[1] < MINIMUM_THRESHOLD and cl.raw[2] < MINIMUM_THRESHOLD

    if debug and lifted:
        print("Robot lifted.", file = stderr)

    return lifted


# --------------------------------------------------------------------------------
#  Main routine.
# --------------------------------------------------------------------------------

def main():

    print('Starting Program..', file=stderr)
    os.system('setfont Lat15-TerminusBold14')

    cl = ColorSensor() 

    debug = constants.DEBUG | constants.DEBUG_THREAD_LIFECYCLE

    with open('data.json') as json_file:  
    
        data = json.load(json_file)


        threadPool = []
        stop_threads = False


        for process in data['steps']:

            inParallel = False if process['step'] == 'launchInSerial' else True
            thread = threading.Thread(target = launchSteps, args = (debug, lambda: stop_threads, process, inParallel))
            threadPool.append(thread)
            thread.start()


        #    while not ts.is_pressed:
            allThreadsCompleted = False

            while not allThreadsCompleted:

                for thread in threadPool:
                    if not thread.isAlive():
                        threadPool.remove(thread)

                if not threadPool:
                    allThreadsCompleted = True
                sleep (0.01) # Give the CPU a rest

                if isRobotLifted(debug):
                    stop_threads = True
                
                #print("b", file=stderr)

            if stop_threads:
                break
                
    print('Finished.', file = stderr)
    #sleep(15)

if __name__ == '__main__':
    main()