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
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.recv()
    if msg: # msg == None if timeout in recv()
        if msg == b'lap':
            db = e.peers_table[host][0]
            # print(host,msg)
            print(db)
            flash(0.1)