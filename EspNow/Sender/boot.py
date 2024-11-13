import network
import espnow
import utime

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of multicast 
e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")

while True:
    try:
        e.send(peer,"lap")
        utime.sleep_ms(1000)
        pass
    except:
        break

    