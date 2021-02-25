from machine import Pin,PWM
from time import sleep

class _Motor():
    def __init__(self,a=14,b=15):
        self.a=Pin(a,Pin.OUT)
        self.b=Pin(b,Pin.OUT)
        self.pwma=PWM(self.a)
        self.pwmb=PWM(self.b)
        self.pwma.freq(500)
        self.pwmb.freq(500)
        self.stop()
    
    def stop(self):
        self.pwma.duty_u16(0)
        self.pwmb.duty_u16(0)
        self.a.low()
        self.b.low()
    
    def forward(self,speed=100):
        self.pwma.duty_u16((speed*65535)//100)
        self.pwmb.duty_u16(0)
        
    def backward(self,speed=100):
        self.pwmb.duty_u16((speed*65535)//100)
        self.pwma.duty_u16(0)

class Robot():
    def __init__(self,l1=14,l2=15,r1=17,r2=16):
        self.l=_Motor(l1,l2)
        self.r=_Motor(r1,r2)
        
    def forward(self,speed=100):
        self.l.forward(speed)
        self.r.forward(speed)
        
    def backward(self,speed=100):
        self.l.backward(speed)
        self.r.backward(speed)
        
    def right(self,speed=100): 
        self.l.forward(speed)
        self.r.backward(speed)

    def left(self,speed=100): 
        self.r.forward(speed)
        self.l.backward(speed)

    def stop(self): 
        self.l.stop()
        self.r.stop()
    
if __name__== '__main__':
    print ('Robot Test')
    robot=Robot()
    while True:
        print("Back")
        robot.backward(75)
        sleep(1)
        print("Forward")
        robot.forward(75)
        sleep(1)
        print("left")
        robot.left(75)
        sleep(1)
        print("right")
        robot.right(75)
    
        sleep(1)
        print("Stop")
        robot.stop()
        sleep(5)
    
    