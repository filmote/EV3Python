#!/usr/bin/env python3

from ev3dev2.sensor.lego import ColorSensor
from sys import stderr

import threading
import time
import constants


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

    cl = ColorSensor() 
    lifted = cl.raw[0] < constants.LIFTED_MINIMUM_THRESHOLD and cl.raw[1] < constants.LIFTED_MINIMUM_THRESHOLD and cl.raw[2] < constants.LIFTED_MINIMUM_THRESHOLD

    if debug and lifted:
        print("Robot lifted.", file = stderr)

    return lifted