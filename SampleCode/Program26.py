#!/usr/bin/env python3
ham = 0b0001
cheese = 0b0010
tomato = 0b0100
bread = 0b1000

mySandwich = ham + cheese + bread

print("Your sandwhich has ", end="")
print(tomato)
if mySandwich & ham:
    print("ham ", end="")
if mySandwich & cheese:
    print("cheese ", end="")
if mySandwich & tomato:
    print("tomato ", end="")
if mySandwich & bread:
    print("bread ", end="")
