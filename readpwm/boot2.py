import usocket as socket

import network

from machine import Pin
import machine


import esp
esp.osdebug(None)

import gc
gc.collect()

local_IP       = '192.168.4.1'
gateway        = '192.168.4.0'
subnet         = '255.255.255.0'
dns            = '8.8.8.8'

ssidAP = 'RCWebServer'
passwordAP = '12345678'

rederPin=Pin(2,Pin.IN)

ap = network.WLAN(network.AP_IF)

ap.config(essid=ssidAP,password=passwordAP)
ap.ifconfig([local_IP,gateway,subnet,dns])
ap.active(True)

while ap.active() == False:
  pass

print('Ap Active')
print(ap.ifconfig())

def read_sensor():
    value = machine.time_pulse_us(rederPin, 1,1000000)
    return value
    
def web_page():
    sensorValue = read_sensor()
    html = """
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
      </head>
      <body>
        <h1>measured pulse : """+ str(sensorValue) + """</h1> 
      </body>
    </html>"""
    return html

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
      conn, addr = s.accept()
      #print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      #print('Content = %s' % str(request))
      response = web_page()
      conn.send(response)
      conn.close()
      pass
except Exception as e:
    print (e)
    s.close()
    pass