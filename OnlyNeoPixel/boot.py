from machine import Pin
import neopixel

pin = Pin(2, Pin.OUT)

global np
np = neopixel.NeoPixel(pin, 8)
for j in range(0,8):
    np[j]=20
    np.write()
