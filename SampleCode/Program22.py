#!/usr/bin/env python3

import xml.etree.ElementTree as ET

from ev3dev2.sensor.lego import ColorSensor
from sys import stderr


def main():
    
    cl = ColorSensor()

    # Load programs ..
    programsXML = ET.parse('Program22_programs.xml')
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

            print('Colour sensor {} compared to {} ({}, {}, {}) result ({}, {}, {})'.format(rgb, programName, rProgram, gProgram, bProgram, rColourSensor - rProgram, gColourSensor - gProgram, bColourSensor - bProgram), file = stderr)

            if abs(rColourSensor - rProgram) < 20 and abs(gColourSensor - gProgram) < 20 and abs(bColourSensor - bProgram) < 20:

                print('Run program {}'.format(program.get('fileName')), file=stderr)

    
if __name__ == '__main__':
    main()