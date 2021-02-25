import time
#import rp2 
#from rp2 import PIO, asm_pio
from machine import Pin
from motor import Robot
from SR04Pio import SR04
sm=SR04()
line=Pin(28,Pin.IN)
robot=Robot()
try:
    while True:
        print("Distance",sm.get())
        print ("Line",line.value())
        dist=sm.get()
        if dist>150:     #nothing within range continue forward @ full speed
            robot.forward()
    #        right.forward()
        elif dist >75:  # obstiacle between 7.5 & 15 CM (approx) start avoiding action
            robot.left() #start to turn
            time.sleep(.25)   #wait .25 seconds to ensure suficient rotation.
        else:
            robot.stop() #obasacle way too close - stop
    #        right.forward()

            
        time.sleep(.1)
except:
    '''Something went wrong!'''
    print("Stoping Motors")
    robot.stop()
