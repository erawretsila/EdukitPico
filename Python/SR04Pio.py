# SR04PIO.py
# (c) Alister J Ware
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import time
import rp2 
from rp2 import PIO, asm_pio
"""SR04 ultrasonic distance sensor using PIO on Raspberry Pi Pico"""
from machine import Pin

@asm_pio(set_init=(PIO.IN_LOW),sideset_init=PIO.OUT_LOW)
def _SR04_PIO():
    """Pio assembler for SR04 ultrasonic assembler"""

    pull() .side(0)         #trigger ping
    mov(y,osr).side(1) [7]  #use trigger as timeout value :-)
    set(x,0)[7]             #x register as echo count
    jmp(y_dec,'wait') .side(0)     #decrement y so no longer 0
    label('wait')
    jmp(pin,'echo')         #pin high so start timing
    jmp(y_dec,'wait')       #jmp if != & then dec y
    label('echo')           #start timing
    jmp(x_dec,'skip') .side(0)       #decrement x & continue
    label('skip')
    jmp(pin,'echo')         #pin still high so loop again
    mov(isr,invert(x))      #invert x & dest to output
    push()                  #output data
    wrap()

class SR04(object):
    def __init__(self,trigger=1,echo=0,sm=0):
        echopin=Pin(echo,Pin.IN)
        print(echopin)
        self.sm=rp2.StateMachine(sm,_SR04_PIO,freq=343000,set_base=echopin,jmp_pin=echopin,sideset_base=Pin(trigger))
        self.sm.active(1)
        self.sm.put(2550)   #trigger initial ping    

    def get(self):
            result=self.sm.get()
            self.sm.put(2550)   #trigger next ping
            return result      #return result

    def activate(self):
        self.sm.activate(1)
        self.sm.put(2550)
    
    def deactivate(self):
        self.sm.deactivate()
        


if __name__=="__main__":
    sm=SR04(26,27)
    while True:
#        sm.put(255)
        print(sm.get())
        time.sleep(.25)
