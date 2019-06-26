#!/usr/bin/env python3
import threading

innerArray = [1,2,3]
outerArray = [innerArray, 4, 5]

for element in outerArray:
  print("{}, ".format(element), end = "")

print("".format(element))

for element in outerArray:

  if isinstance(element, list):

    for subElement in element:
        print("subElement {}, ".format(subElement), end = "")

  else:
    print("element {}, ".format(element), end = "")

print("".format(element))
