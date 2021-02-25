import time
import rp2 
from rp2 import PIO, asm_pio
"""SR04 ultrasonic distance senso using PIO on Raspberry Pi Pico"""
from machine import Pin

@asm_pio(set_init=(PIO.IN_LOW),sideset_init=PIO.OUT_LOW)
def _SR04_PIO():
    """Pio assembler for SR04 ultrasonic assembler"""
    label ('start')
    wait(0,pin,0)              #check echo pin is low befor starting
    mov(x,null) .side(1)[7]    #set trigger pin high & clear x register
    nop() .side(0)             #return trigger to low
    wait(1,pin,0)              #wait for start of echo pulse
    label('countdown')
    jmp(x_dec,'skip')          #decrement x reg
    label('skip')             
    jmp(x,'exit')              #exit if x 0 #time out
    jmp(pin,'countdown')       #ping still high continue counting
    mov(isr, invert(x))        #invert x & prepare to output
    push()                     #output to Fifo
    label ('exit')
    jmp ('start')              #echo has tmed out, return to start.

class SR04(object):
    def __init__(self,trigger=1,echo=0):    
        self.sm=rp2.StateMachine(1,_SR04_PIO,freq=500000,set_base=Pin(echo),sideset_base=Pin(trigger))
        self.sm.active(1)
    
    def get(self):
        return self.sm.get()
    
    def activate(self):
        self.sm.activate()
    
    def deactivate(self):
        self.sm.deactivate()
        


if __name__=="__main__":
    sm=SR04()
    while True:
        print(sm.get())
        time.sleep(.1)