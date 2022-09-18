from MicroWebSrv2  import *
from time          import sleep

import network

from machine import Pin
import machine
import os

global rtc
rtc = machine.RTC()
#(2022, 9, 16, 4, 22, 12, 1, 567677)
#(year, month, day, weekday, hour, minute, second, microseconds)
rtc.datetime((1993, 8, 25, 1, 10, 10, 1, 1))
global passtime
passtime = rtc.datetime()
global currentTime
currentTime = rtc.datetime() 
global started 
started = False

#hardware pin config
rederPin=Pin(2,Pin.IN)
#gloabal variable
global previousValue
global value

previousValue = 0
value = 0

local_IP       = '192.168.4.1'
gateway        = '192.168.4.0'
subnet         = '255.255.255.0'
dns            = '8.8.8.8'

ssidAP = 'RCWebServer'
passwordAP = '12345678'

ap = network.WLAN(network.AP_IF)

ap.config(essid=ssidAP,password=passwordAP)
ap.ifconfig([local_IP,gateway,subnet,dns])
ap.active(True)

while ap.active() == False:
    #wait until active
    pass

# ============================================================================
# ============================================================================
# ============================================================================

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
pass

# ------------------------------------------------------------------------


def measureRadioButtonState() -> tuple(bool, int):
    global previousValue
    global value
    changed = True
    state = 0
    try:
        value = machine.time_pulse_us(rederPin, 1,1000000)
        if isclose(value,previousValue,0,50):
            pass
            changed = False
        else:
            previousValue = value
            changed = True
            pass
        if value > 1000:
            state = 0
        else:
            state = 1
        pass
    except Exception as e:
        print(e)
        changed = False
        state = 0
        pass
    return changed,state
pass

# ------------------------------------------------------------------------

def OnWebSocketAccepted(microWebSrv2, webSocket) :
    print('Example WebSocket accepted:')
    print('   - User   : %s:%s' % webSocket.Request.UserAddress)
    print('   - Path   : %s'    % webSocket.Request.Path)
    print('   - Origin : %s'    % webSocket.Request.Origin)
    
    
    if webSocket.Request.Path.lower() == '/wstest' :
        webSocket.OnTextMessage   = OnWebSocketTextMsg
        webSocket.OnBinaryMessage = OnWebSocketBinaryMsg
        webSocket.OnClosed        = OnWebSocketClosed

    while webSocket is not None:
        sleep(1)
        webSocketSendState(webSocket)
        pass

# ------------------------------------------------------------------------

def webSocketSendState(webSocket):
    global started
    global passtime
    global currentTime
    timeString = ""
    state = measureRadioButtonState()
    #print('State changed: '+ str(state[0]) +' Received State: '+ str(state[1]))
    if state[0] == True :
        if state[1] == 1:
            print("-----------gris-----------")
            if started:
                currentTime = rtc.datetime()
                ms =  round(currentTime[5]*60000000 + currentTime[6]*1000000 + currentTime[7])
                pms =  round(passtime[5]*60000000 + passtime[6]*1000000 + passtime[7])
                passtime = currentTime
                racetime = abs(pms - ms)
                seconds = abs(round(racetime / 1000000))
                minutes = abs(round(racetime / 60000000))
                if (seconds > 59):
                    seconds = seconds % 60
                    minutes += round(seconds / 60)
                    pass
                milliseconds = racetime % 1000
                if (minutes < 10):
                    timeString += "0"
                    pass
                timeString += str(minutes)
                timeString += ":"
                if (seconds < 10):
                    timeString += "0"
                    pass
                timeString += str(seconds)
                timeString += "."
                timeString += str(milliseconds)
                print(str(timeString))
                started = False
                print("stopped currentTime" + str(currentTime))
                print("stopped passtime" + str(passtime))
                pass
            else : 
                print("waiting")
                print("currentTime" + str(currentTime))
                print("passtime" + str(passtime))
                pass
        elif state[1] == 0:
            print("---------orange-------------")
            if not started:
                passtime = rtc.datetime()
                started = True
                print("started passtime" + str(passtime))
            pass
        pass
        if timeString != "":
            webSocket.SendTextMessage('TIME: "%s"' % str(timeString))

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

def OnWebSocketTextMsg(webSocket, msg) :
    print('WebSocket text message: %s' % msg)
    webSocket.SendTextMessage('Received "%s"' % msg)

# ------------------------------------------------------------------------

def OnWebSocketBinaryMsg(webSocket, msg) :
    print('WebSocket binary message: %s' % msg)

# ------------------------------------------------------------------------

def OnWebSocketClosed(webSocket) :
    print('WebSocket %s:%s closed' % webSocket.Request.UserAddress)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

print()

# Loads the WebSockets module globally and configure it,
wsMod = MicroWebSrv2.LoadModule('WebSockets')
wsMod.OnWebSocketAccepted = OnWebSocketAccepted

# Instanciates the MicroWebSrv2 class,
mws2 = MicroWebSrv2()

# For embedded MicroPython, use a very light configuration,
mws2.SetEmbeddedConfig()

# All pages not found will be redirected to the home '/',
mws2.NotFoundURL = '/'

# Starts the server as easily as possible in managed mode,
mws2.StartManaged()

# Main program loop until keyboard interrupt,
try :
    while mws2.IsRunning :
        sleep(1)
except KeyboardInterrupt :
    pass

# End,
print()
mws2.Stop()
print('Bye')
print()

# ============================================================================
# ============================================================================
# ============================================================================