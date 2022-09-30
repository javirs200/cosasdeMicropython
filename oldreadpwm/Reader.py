from time import sleep_ms
from machine import Pin
import machine
import os


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
pass


print(os.listdir())

rederPin=Pin(2,Pin.IN)
previousValue = 0
try:
    while True:
        value = machine.time_pulse_us(rederPin, 1,1000000)
        if isclose(value,previousValue,0,50):
            pass
        else:
            previousValue = value
            if value > 1000:
                print("pressed orange")
            else:
                print("pressed gray")
            pass
except Exception as e:
    print(e)
    pass
