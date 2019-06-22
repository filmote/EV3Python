#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from sys import stderr
from time import sleep

xmlDocument = ET.parse('Program19_data.xml')
steps = xmlDocument.getroot()

for step in steps:

    action = step.get('action')
    print("action = {}".format(action), file=stderr )
