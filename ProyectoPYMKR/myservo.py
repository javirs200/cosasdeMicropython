
from machine import Pin,PWM

class myServo(object):
    
    def __init__(self, pin: int=15, hz: int=50, duty: int=512):
        self._servo = PWM(Pin(pin),hz,duty)
        self._in1Pin=Pin(12, Pin.OUT)
        self._in2Pin=Pin(14, Pin.OUT)
        self._enablePin=Pin(13, Pin.OUT)
        self._pwm=PWM(self._enablePin,10000,512)

    def myServoWriteDuty(self, duty):
        if duty <= 26:
            duty = 26
        if duty >= 128:
            duty = 128
        self._servo.duty(duty)
        
    def myServoWriteAngle(self, pos):
        if pos <= 0:
            pos = 0
        if pos >= 180:
            pos = 180
        pos_buffer=(pos/180)*(128-26)
        self._servo.duty(int(pos_buffer)+26)

    def myServoWriteTime(self, us):
        if us <= 500:
            us = 500
        if us >= 2500:
            us = 2500
        pos_buffer=(1024*us)/20000
        self._servo.duty(int(pos_buffer))
        
    def deinit(self):
        self._servo.deinit()
        
    def driveMotor(self,dirc,spd):
        if dirc:
            self._in1Pin.value(1)
            self._in2Pin.value(0)
        else :
            self._in1Pin.value(0)
            self._in2Pin.value(1)
        self._pwm.duty(spd)
