#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from time import sleep
from sys import stderr

import xml.etree.ElementTree as ET
import threading
import time
import types
from sys import stderr


def main():
    
    ts = TouchSensor()
    cl = ColorSensor()

    while (True):
        rgb = cl.raw   
        print(rgb, file=stderr)


if __name__ == '__main__':
    main()