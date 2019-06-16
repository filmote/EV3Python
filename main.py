#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from time import sleep
from sys import stderr

import threading
import time
import os
import json

from functions import DelayForXSeconds
from functions import ReturnWhenObjectWithinXcm



# --------------------------------------------------------------------------------
#  Launch an individual step.
#
#  Launches an individual stepThe details of the 'process' node are quired to determine what step to launch.
#  
# 
#  Parameters:      
#
#  debug        - If in debug mode, details will be printed to the console.
#  stop         - Should the process be stopped?
#  action       - JSON process node.  
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

    
def launchSteps(debug, stop, actions, inParallel = True):

    threadPool = []
    threadPoolTotalCount = 0
    threadPoolCount = 0
    stepCount = 0

    stop_threads = False
    

    # Launch the process(es) for this step.  If the 
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


    if 'steps' not in actions:

        newThread = launchStep(debug, stop, actions)
        threadPool.append(newThread)
        threadPoolCount = 1


    threadPoolTotalCount = threadPoolCount
    allThreadsCompleted = False

    while not allThreadsCompleted:

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
        print("a", file=stderr)

    for thread in threadPool:
        thread.join()


def isRobotLifted(debug):

    MINIMUM_THRESHOLD = 2
    cl = ColorSensor() 

    lifted = cl.raw[0] < MINIMUM_THRESHOLD and cl.raw[1] < MINIMUM_THRESHOLD and cl.raw[2] < MINIMUM_THRESHOLD

    if debug and lifted:
        print("Robot lifted.", file = stderr)

    return lifted


def main():

    print('Starting Program..', file=stderr)
    os.system('setfont Lat15-TerminusBold14')

    cl = ColorSensor() 

    debug = True

    with open('data.txt') as json_file:  
    
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
                
                print("b", file=stderr)
                    
            for thread in threadPool:
                thread.join()

            if stop_threads:
                break
                
    print('Finished.', file = stderr)
    #sleep(15)

if __name__ == '__main__':
    main()