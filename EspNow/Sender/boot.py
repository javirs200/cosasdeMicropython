import network
import espnow

from machine import Pin
from utime import sleep

led=Pin(2,Pin.OUT) # onboard led
led.value(0)

def flash(speed):
    for i in range(3):
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

print("espnow peer conection...")

e.send(peer, "Starting...")

print("starting to send lap ping")

while True:
    try:
        response = e.send(peer,"lap")
        flash(0.1)
        sleep(1)
        pass
    except:
        break

    