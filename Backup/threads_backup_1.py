#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, InfraredSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from time import sleep

import threading
import time
import os

def delayForXSeconds(id, stop, delayLength):

    print("Starting delayForXSeconds thread {}".format(id))

    start_time = time.time()

    while time.time() < start_time + delayLength:

        if stop():
            print("Exiting delayForXSeconds.")
            break

    print("Clean up.")

def returnWhenObjectWithin25cm(id, stop):

    ir = InfraredSensor() 

    print("Starting returnWhenObjectWithin25cm thread {}".format(id))
    while True:

        if ir.proximity < 50:
            print("Clean up.")
            break

        if stop():
            print("Exiting returnWhenObjectWithin25cm.")
            break


def main():

    os.system('setfont Lat15-TerminusBold14')

    ir = InfraredSensor() 
    ts = TouchSensor()
    leds = Leds()

    workers = []

    stop_threads = False

    for id in range(0, 3):
        tmp = threading.Thread(target=returnWhenObjectWithin25cm, args=(id, lambda: stop_threads))
        workers.append(tmp)
        tmp.start()
    tmp = threading.Thread(target=delayForXSeconds, args=(id, lambda: stop_threads, 20))
    workers.append(tmp)
    tmp.start()


#    while not ts.is_pressed:
    allThreadsCompleted = False

    while not allThreadsCompleted:
        print(threading.activeCount())
        for worker in workers:
            if not worker.isAlive():
                workers.remove(worker)
        if not workers:
            allThreadsCompleted = True
            stop_threads = True
        sleep (0.01) # Give the CPU a rest

    for worker in workers:
        worker.join()
    print('Finis.')
    sleep(15)

if __name__ == '__main__':
    main()