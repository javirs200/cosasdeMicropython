from machine import Pin
import neopixel
import time
pin = Pin(2, Pin.OUT)
np = neopixel.NeoPixel(pin, 8)

brightness=1         #brightness: 0-1.0
red=0                  #red
green=0                #green
blue=0                 #blue


try:        
    for i in range(0,255):
        for j in range(0,8):
            np[j]=(int(0),int(0),int(0))
            np.write()
        time.sleep_ms(2)
except Exception as e:
    print("error excepcion \n" + e)