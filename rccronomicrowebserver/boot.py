from MicroWebSrv2  import *
from time          import sleep
import uasyncio
import network
from machine import Pin
from machine import RTC
from machine import time_pulse_us
from RsmaxUtils  import *
from RsmaxUtils.mynetwork.networkManager import myNetwork


global rtc
rtc = RTC()
#(2022, 9, 16, 4, 22, 12, 1, 567677)
#(year, month, day, weekday, hour, minute, second, microseconds)
rtc.datetime((1993, 8, 25, 1, 10, 10, 1, 1))
global passtime
passtime = rtc.datetime()
global currentTime
currentTime = rtc.datetime() 
global started 
started = False
global sended 
sended = False

#hardware pin config
rederPin=Pin(2,Pin.IN)
rederPin2=Pin(0,Pin.IN)
#gloabal variable
global previousValue1
global previousValue2
global value1
global value2
global timeString

timeString = ""

previousValue1 = 0
previousValue2 = 0
value1 = 0
value2 = 0


# ------------------------------------------------------------------------


def measureRadioButtonState() -> tuple(bool, int,int):
    global previousValue1
    global previousValue2
    global value1
    global value2
    changed = False
    state1 = 0
    state2 = 0
    try:
        value1 = time_pulse_us(rederPin, 1,1000000)
        value2 = time_pulse_us(rederPin2, 1,1000000)
        cambio1 = isclose(value1,previousValue1,0,50)
        cambio2 = isclose(value2,previousValue2,0,50)
        if cambio1 or cambio2:
            pass
            changed = False
        else:
            if cambio1:
                previousValue1 = value1
                pass
            if cambio2:
                previousValue2 = value2
                pass
            changed = True
            pass
        if value1 > 1000:
            state1 = 0
        else:
            state1 = 1
        pass
        if value2 > 1000:
            state2 = 0
        else:
            state2 = 1
        pass
    except Exception as e:
        print(e)
        changed = False
        state1 = 0
        state2 = 0
        pass
    return changed,state1,state2
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
        sleep(0.2)
        webSocketSendState(webSocket)
        pass

# ------------------------------------------------------------------------

def webSocketSendState(webSocket):
    global started
    global passtime
    global currentTime
    global timeString
    global sended
    state = measureRadioButtonState()
    if state[0] == True :
        if state[1] == 1:
            #print("-----------gris-----------")
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
                print('TIME: "%s"' % str(timeString))
                if timeString != "":
                    webSocket.SendTextMessage('TIME: "%s"' % str(timeString))
                    pass
                sended = False 
                started = False
            else: 
                #print("waiting")
                pass
        elif state[1] == 0:
            #print("---------orange-------------")
            if not started:
                passtime = rtc.datetime()
                started = True
                timeString = ""
            pass
        if state[2] == 0:
            if not sended:
                if timeString != "":
                    uasyncio.run(append_new_line("data.txt",str(timeString)))
                    print('triggered chanel 4 Write to file: "%s"' % str(timeString))
                    webSocket.SendTextMessage('Write to file: "%s"' % str(timeString))
                    sended = True
                    pass
                pass
            pass
    pass
        

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

def OnWebSocketTextMsg(webSocket, msg) :
    print('WebSocket text message: %s' % msg)
    webSocket.SendTextMessage('msg "%s"' % str(msg))

# ------------------------------------------------------------------------

def OnWebSocketBinaryMsg(webSocket, msg) :
    print('WebSocket text message: %s' % msg)

# ------------------------------------------------------------------------

def OnWebSocketClosed(webSocket) :
    print('WebSocket %s:%s closed' % webSocket.Request.UserAddress)

# ------------------------------------------------------------------------


#......................main.................

net = myNetwork()
print('phase 0 , wifi scan')
net.connectOrReconect()

print("server started")

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