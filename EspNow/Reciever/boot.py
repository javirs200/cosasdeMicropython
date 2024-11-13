import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

while True:
    try:
        host, msg = e.recv()
        if msg: # msg == None if timeout in recv()
            db = e.peers_table[host][0]
            # print(host,msg)
            print(db)
    except:
        break
        