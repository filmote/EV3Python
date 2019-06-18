#!/usr/bin/env python3

from sys import stderr
import json


def minimise(file_name):

    minimisedData = ''
    inMultilineComment = False
    
    f = open(file_name, "r")

    for x in f:

        idx = 0
        x = x.strip()
    
        if x.startswith("/*"):
            inMultilineComment = False if "*/" in x else True
    
        elif x.startswith('//'):
            pass
    
        elif "/*" in x:
            minimisedData = minimisedData + x[0 : x.find("/*")].strip()
            inMultilineComment = False if "*/" in x else True
    
        elif "*/" in x:
            inMultilineComment = False
    
        elif "//" in x:
            minimisedData = minimisedData + x[0 : x.find("//")].strip()
    
        elif inMultilineComment and "*/" in x:
            inMultilineComment = False
    
        else:
            if not inMultilineComment:        
                minimisedData = minimisedData + x

    f.close()

    return json.loads(minimisedData)