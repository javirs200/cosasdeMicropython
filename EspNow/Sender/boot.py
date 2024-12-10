import network
import espnow

from machine import Pin
from utime import sleep

led=Pin(2,Pin.OUT) # onboard led
led.value(0)

def flash(speed):
        led.value(1)
        sleep(speed)
        led.value(0)
        sleep(speed)

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of multicast 
e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")

while True:
    try:
        response = e.send(peer,"lap")
        flash(0.005) # inerit sleep of 2 x parameter
        pass
    except:
        break