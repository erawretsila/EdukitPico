# -*- coding: utf-8 -*-
#
#  Edukit3.py
#  
#  Copyright 2021  alister.ware@ntlworld.com
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
from machine import Pin
from motor import Robot
from SR04Pio2 import SR04
from IRDecode_RC6 import RC6


def remote(sensors):
    print('doing remote')
    key=sensors['ir'].lastkey & 0xff
    keytime=sensors['ir'].keytime
    print(key)
    if keytime+1 <time.time(): # 1 second or more since lat keypress
        robot.stop()
        return
    if key ==0x22:
        robot.stop()
    if key ==0x1e:
        robot.forward(100)
    if key ==0x1f:
        robot.backward(100)
    if key ==0x20:
        robot.left(100)
    if key==0x21:
        robot.right(100)
    return

def avoid(sensors):
    dist=sensors['dist'].result
    if dist>150:
        robot.forward()
#        right.forward()
    elif dist >75:
        robot.left()
        time.sleep(.25) #ottion time
    else:
        robot.stop()
#        right.forward()

def seek():
    print ("Seeking Line")
    direction =True
    seektime = .1
    seekcount = 1
    maxseek = 5
    print(seekcount)
    while seekcount <maxseek:
        if direction:
            print("left")
            robot.left(75)
        else:
            print ("right")
            robot.right(75)
        starttime=time.time()
        while time.time()-starttime <=seektime:
            if not line.value():
                robot.stop()
                return True
        robot.stop()
        seekcount += 1
        direction = not direction
        seektime+=.1
        print(direction,seekcount)
    return False

def line_follow(sensors):
    if not line.value():
        robot.forward()
    else:
        seek()


sr04=SR04(26,27)
line=Pin(21,Pin.IN)
robot=Robot()
mode ='ir'
ir=RC6(18)
sensors={'ir':ir,'dist':sr04,'line':line}
action={'dist':avoid,'ir':remote,'line':line_follow}

  
print ('initialisation complete')
#print(sm)
while True:
    if time.time() <ir.keytime+1:  #recent key press
        print ('should not be here long')   
        key=ir.lastkey&0xff
        print (hex(key))
        if key ==12:
            print ('stop')
            mode='stop'
            robot.stop()
            
        if key  ==0x50:
            mode='ir'
            print('Remote Control')
        if key ==0x47:
            mode='dist'
            print('Avoidance')
        if key ==0x4a:
            mode='line'
            print ("line follow")
        if key==0x0f:
            print (sr04.get())
#            time.sleep(.5) # delay to make op readable
    if mode=='stop':
        continue
    action[mode](sensors)            
    time.sleep(.1)

