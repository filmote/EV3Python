#!/usr/bin/env python3

from sys import stderr

# simplest case
print('EV3 Python')

# with a single or multiple substitution
print('EV3 {}'.format('Python'))
print('{} {}'.format('EV3', 'Python'))

# printing variables
firstWord = 'EV3'
secondWord = 'Python'
print('{} {}'.format(firstWord, secondWord))

# using the end="" parameter to print on a single line
print('{} '.format(firstWord), end="")
print('{}'.format(secondWord))

# printing to the VSCode console
