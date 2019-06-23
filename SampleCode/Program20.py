#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from time import sleep

def printAction(step):

    action = step.get('action')
    motor = step.get('motor')
    speed = float(step.get('speed'))
    seconds = float(step.get('seconds'))

    print("action = {}".format(action), end="" )
    print(", motor = {}".format(motor), end="" )
    print(", speed = {}".format(speed), end="" )
    print(", seconds = {}".format(seconds) )


def loopThroughXML(steps):

    for step in steps:

        action = step.get('action')

        if action == 'launchInParallel':
            loopThroughXML(step)

        else:
            printAction(step)

def main():

    xmlDocument = ET.parse('Program20_data.xml')
    steps = xmlDocument.getroot()
    loopThroughXML(steps)
    sleep(5)
   

if __name__ == '__main__':
    main()