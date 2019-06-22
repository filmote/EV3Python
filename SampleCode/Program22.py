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

            rProgram = int(program.get('r'))
            gProgram = int(program.get('g'))
            bProgram = int(program.get('b'))

            print('RGB {} compared to {} {} {} = {} {} {}'.format(rgb, rProgram, gProgram, bProgram, rgb[0] - rProgram, rgb[1] - gProgram, rgb[2] - bProgram), file = stderr)

            if abs(rgb[0] - rProgram) < 20 and abs(rgb[1] - gProgram) < 20 and abs(rgb[2] - bProgram) < 20:

                print('Run prgogram {}'.format(program.get('fileName')), file=stderr)


    
if __name__ == '__main__':
    main()