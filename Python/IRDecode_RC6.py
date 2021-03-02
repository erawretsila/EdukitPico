# IRDecode_RC6.py
# (c) Alsier J Ware
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
import time

import rp2
from rp2 import PIO, asm_pio
from machine import Pin

@asm_pio(set_init=(PIO.IN_LOW))
def RC6PIO():
    label('start')
    pull()
    mov(y,osr)
#    mov(isr,0)
    wait(0,pin,0) 
    wait(1,pin,0) [7]
#    wait(1,pin,0)
    label('low')
    jmp(y_dec,'cont')
    jmp('exit')
    label('cont')
    wait (0,pin,0)
    set(x,0)
    in_(x,1) [7]
    jmp(pin,'low')
    label('high')
    jmp(y_dec,'conth')
    jmp('exit')
    label('conth')
    wait(1,pin,0)
    set(x,1)
    in_(x,1) [7]
    jmp(pin,'low')
    jmp('high')
    label('exit')
    push()
    irq(noblock,rel(0))
    jmp('start')
      
class RC6()  :
    def __init__(self,ir=0,sm=5):
        irpin=Pin(ir,Pin.IN)
        self.sm=rp2.StateMachine(sm,RC6PIO,freq=1400*12,in_base=irpin,jmp_pin=irpin)
        self.sm.active(1)
        self.lastkey=0
        self.keytime=0
        self.sm.irq(self.get_ir)
        self.sm.put(0x25)
        
    def get_ir(self,*args):
        self.lastkey=self.sm.get()
#        self.keytime=time.time()
        self.sm.put(0x25)

if __name__=='__main__':
    from time import sleep
    '''module diagnostics'''
    rc6=RC6(18)
#    print(dir(rc6.sm))

    while True:
#        print(rc6.lastkey)
        time.sleep(1)
        print (hex(rc6.lastkey &0x7f),rc6.keytime)
