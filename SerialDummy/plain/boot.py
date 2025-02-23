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

async def serialManager():
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
            if char == '\n':
                print("msg:",msg )
                msg = ""
                            
        await uasyncio.sleep(0.01)

async def printDummy():
    msg = ""
    while True:
        
        print("dummy message")
                  
        await uasyncio.sleep(2)

def main():

    try:
        loop = uasyncio.get_event_loop()
        loop.create_task(serialManager())
        loop.create_task(printDummy())
        loop.run_forever()
    except Exception as e:
        print('Exception ',e)
        loop.stop()
        loop.close()

if __name__ == "__main__":
    main()
        