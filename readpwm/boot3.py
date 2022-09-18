from MicroWebSrv2 import *
from time         import sleep

import network

local_IP       = '192.168.4.1'
gateway        = '192.168.4.0'
subnet         = '255.255.255.0'
dns            = '8.8.8.8'

ssidAP = 'RCWebServer'
passwordAP = '12345678'

def OnWebSocketAccepted(microWebSrv2, webSocket) :
    print('Example WebSocket accepted:')
    print('   - User   : %s:%s' % webSocket.Request.UserAddress)
    print('   - Path   : %s'    % webSocket.Request.Path)
    print('   - Origin : %s'    % webSocket.Request.Origin)
    

ap = network.WLAN(network.AP_IF)

ap.config(essid=ssidAP,password=passwordAP)
ap.ifconfig([local_IP,gateway,subnet,dns])
ap.active(True)

while ap.active() == False:
  pass

print('Ap Active')
print(ap.ifconfig())

wsMod = MicroWebSrv2.LoadModule('WebSockets')
wsMod.OnWebSocketAccepted = OnWebSocketAccepted


mws2 = MicroWebSrv2()
mws2.SetEmbeddedConfig()
mws2.NotFoundURL = '/'
mws2.StartManaged()

# Main program loop until keyboard interrupt,
try :
    while True :
        sleep(1)
except KeyboardInterrupt :
    mws2.Stop()