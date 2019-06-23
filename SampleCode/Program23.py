#!/usr/bin/env python3

import xml.etree.ElementTree as ET

from ev3dev2.sensor.lego import ColorSensor
from sys import stderr


def main():
    
    cl = ColorSensor()

    # Load programs ..
    programsXML = ET.parse('Program23_programs.xml')
    programs = programsXML.getroot()
    
    while True:

        rgb = cl.raw

        for program in programs:

            programName = program.get('name')
            rProgram = int(program.get('r'))
            gProgram = int(program.get('g'))
            bProgram = int(program.get('b'))

            rColourSensor = rgb[0]
            gColourSensor = rgb[1]
            bColourSensor = rgb[2]

            if abs(rColourSensor - rProgram) < 20 and abs(gColourSensor - gProgram) < 20 and abs(bColourSensor - bProgram) < 20:

                fileName = program.get('fileName')

                
                # Load program into memory ..

                dataXML = ET.parse(fileName)
                steps = dataXML.getroot()

                for step in steps:

                    print(step.get('name'))

    
if __name__ == '__main__':
    main()