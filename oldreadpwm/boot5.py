from MicroWebSrv2  import *
from time          import sleep

import network

from machine import Pin
import machine
import os

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
    state = measureRadioButtonState()
    print('State changed: '+ str(state[0]) +' Received State: '+ str(state[1]))
    if state[0] == True :
        webSocket.SendTextMessage('Received State: "%s"' % str(state[1]))

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
