from irrecvdata import irGetCMD
import time
from machine import SoftI2C, Pin
from I2C_LCD import I2cLcd
from  IRdict import IRDICT

DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(14), sda=Pin(13), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

recvPin = irGetCMD(15)
try:
    print(IRDICT.keys())
    lcd.move_to(0, 0)
    lcd.putstr("Hello,world!")
    while True:
        irValue = recvPin.ir_read()
        if irValue:
            lcd.clear()
            lcd.move_to(0, 1)
            lcd.putstr("IR :" + str(IRDICT.get(str(irValue).upper())))
            #print(irValue)
            #print(str(irValue).upper())
            pass
except:
    pass