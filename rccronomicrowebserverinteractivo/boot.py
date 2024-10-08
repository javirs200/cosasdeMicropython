from MicroWebSrv2  import *
from time          import sleep
import uasyncio
import network
from machine import Pin
from machine import RTC
from machine import time_pulse_us
from RsmaxUtils  import *

global Firstload
Firstload = True

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

#hardware pin config
rederPin=Pin(2,Pin.IN)
#gloabal variable
global previousValue1
global value1
global ws
ws = None

previousValue1 = 0
value1 = 0

#ssidAP = 'RCWebServer'
#passwordAP = '12345678'

#ap = network.WLAN(network.AP_IF)
#ap.config(essid=ssidAP,authmode = 3,password=passwordAP) # 3= WPA2-PSK ,0 open
#ap.active(True)

ssidRouter="POCOX6PRO"
passwordRouter="xcom1234"

#ssidRouter     = 'HUAWEI P30 lite' #Enter the router name
#passwordRouter = 'xcom1234' #Enter the router password



sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    sta_if.active(True)
    sta_if.connect(ssidRouter,passwordRouter)
    while not sta_if.isconnected():
        pass

# ------------------------------------------------------------------------


def measureRadioButtonState() -> tuple(bool, int):
    global previousValue1
    global value1
    changed = False
    state1 = 0
    try:
        value1 = time_pulse_us(rederPin, 1,1000000)
        #print(value1,previousValue1)
        cercano = isclose(value1,previousValue1,0,100)
        if not cercano:
            changed = True
            previousValue1 = value1
            if value1 > 1000:
                state1 = 0
            else:
                state1 = 1
            pass  
    except Exception as e:
        print("excepcion cambio ,",e)
        changed = False
        state1 = 0
        pass
    #print("similares",cercano,"cambio de estado",changed)
    return changed,state1
pass

# ------------------------------------------------------------------------

def OnWebSocketAccepted(microWebSrv2, webSocket) :
    global ws
    
    if webSocket.Request.Path.lower() == '/ws' :
        webSocket.OnTextMessage   = OnWebSocketTextMsg
        webSocket.OnBinaryMessage = OnWebSocketBinaryMsg
        webSocket.OnClosed        = OnWebSocketClosed
        print("webSocket requestd") 

    if(webSocket is not None):
        if(ws is None):
            ws = webSocket
    print("webSocket acepted")

# ------------------------------------------------------------------------

def webSocketSendState(webSocket):
    global started
    global passtime
    global currentTime
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
                timeString = formatTime(racetime)
                if timeString != "":
                    #print("send " ,timeString)
                    webSocket.SendTextMessage(str(timeString))
                    #print("sended " ,timeString)
                    pass 
                started = False
            else: 
                #print("waiting")
                pass
        elif state[1] == 0:
            #print("---------orange-------------")
            if not started:
                passtime = rtc.datetime()
                started = True
            pass
    pass
      

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

def OnWebSocketTextMsg(webSocket, msg) :
    #print('WebSocket text message: %s' % msg)
    strmsg = str(msg)
    if "store " in strmsg:
        timstr = remove_prefix(strmsg,'store ')
        uasyncio.run(append_new_line("data.txt",str(timstr)))
       

# ------------------------------------------------------------------------

def OnWebSocketBinaryMsg(webSocket, msg) :
    print('WebSocket text message: %s' % msg)

# ------------------------------------------------------------------------

def OnWebSocketClosed(webSocket) :
    print('WebSocket %s:%s closed' % webSocket.Request.UserAddress)

# ------------------------------------------------------------------------

def doing():
    global ws
    global Firstload
    if(ws is not None):
        if(Firstload):
            uasyncio.run(sendData(ws))
            Firstload = False
        else:
            uasyncio.run(blocante(ws))
        pass
    pass

async def blocante(ws):
    sleep(0.1)
    webSocketSendState(ws)
    pass

#......................main.................

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
        doing()
except KeyboardInterrupt :
    pass

# End,
mws2.Stop()
print('--------Bye-------')


# ============================================================================
# ============================================================================
# ============================================================================