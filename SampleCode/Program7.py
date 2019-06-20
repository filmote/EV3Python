#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, LargeMotor, OUTPUT_B, OUTPUT_C
import threading

def onForSeconds(motor, speed, seconds):
    motor.on_for_seconds(speed, seconds, brake = True, block = True)

def main():

    lm1 = LargeMotor(OUTPUT_B)
    lm2 = LargeMotor(OUTPUT_C)
    mm = MediumMotor()
    
    # create a threadPool array to 'collect' the threads ..
    threadPool = []
    thread1 = threading.Thread(target = onForSeconds, args = (lm1, 30, 4))
    thread2 = threading.Thread(target = onForSeconds, args = (lm2, 40, 3))
    threadPool.append(thread1)
    threadPool.append(thread2)

    # start threads
    thread1.start()
    thread2.start()
    
    # are any threads still working?
    while threadPool:
        for thread in threadPool:
            if not thread.isAlive():
                threadPool.remove(thread)
    
    # All threads are complete, so we can run the next step ..
    threadPool = []
    thread3 = threading.Thread(target = onForSeconds, args = (mm, 10, 6))
    threadPool.append(thread3)

    # start the thread
    thread3.start()
        
    # are any threads still working?
    while threadPool:
        for thread in threadPool:
            if not thread.isAlive():
                threadPool.remove(thread)

if __name__ == '__main__':
    main()