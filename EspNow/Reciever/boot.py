import network
import espnow
import sys
import uasyncio
import uselect

from machine import Pin
from utime import sleep

led=Pin(2,Pin.OUT) # onboard led
led.value(0)

def flash(speed):
        led.value(1)
        uasyncio.sleep(speed)
        led.value(0)
        uasyncio.sleep(speed)

async def serialManager(dbTreshold):
    count = 0
    msg = ""
    while True:
        # read byte(str) from stdin non-blocking
        list = uselect.select([sys.stdin], [], [], 0.01)
        if list[0]:
            char = sys.stdin.read(1)
        else:
            char = None
            
        # build msg
        if char:
            msg = msg + char
            count += 1
            if char == '\n':
                print("msg:",msg , "count:",count)
                if count == 4:
                    newTreshold = int(msg)
                    if newTreshold < 0 and newTreshold != dbTreshold[0]:
                        dbTreshold[0] = newTreshold
                        print("new dbTreshold:",dbTreshold[0])
                count = 0
                msg = ""
                                
        await uasyncio.sleep(0.01)

async def espnowManager(e,dbTreshold,currentLap):
    diff = 0
    while True:
        host,msg = e.recv()
        if msg == b'lap':
            currentmsgData = e.peers_table[host]
            db = currentmsgData[0]
            timestamp = currentmsgData[1]
            if db > dbTreshold[0]:
                diff = timestamp - currentLap
                if diff > 2000:
                    flash(0.01)
                    print("time:", diff)
                currentLap = timestamp
            #debug print it is sended to serial port , remove beroe production
            #print("db:",db,"timestamp:",timestamp,"currentLap:",currentLap,"diff:",diff)
        await uasyncio.sleep(0.01)

def main():
    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

    e = espnow.ESPNow()
    e.active(True)

    currentLap = 0
    dbTreshold = [-20]

    try:
        loop = uasyncio.get_event_loop()
        loop.create_task(serialManager(dbTreshold))
        loop.create_task(espnowManager(e,dbTreshold,currentLap))
        loop.run_forever()
    except Exception as e:
        print('Exception ',e)
        loop.stop()
        loop.close()

if __name__ == "__main__":
    main()
        