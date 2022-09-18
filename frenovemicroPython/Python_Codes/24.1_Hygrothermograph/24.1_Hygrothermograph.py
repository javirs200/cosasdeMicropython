import machine
import time
import dht

DHT = dht.DHT11(machine.Pin(13))

DHT.measure()

# time.sleep_ms(10)
# DHT.measure()
# time.sleep_ms(10)
# print('temperature:',DHT.temperature(),'humidity:',DHT.humidity())
# 
# try:
#     while True:
#         DHT.measure()
#         print('temperature:',DHT.temperature(),'humidity:',DHT.humidity())
#         time.sleep_ms(1000)
# except Exception as e:
#     print("error " + str(e))
    
    
    

    
    
    
    
    
    
    


