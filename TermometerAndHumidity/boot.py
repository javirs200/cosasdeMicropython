import machine, os, vfs
from time import sleep_ms,sleep

import dht

from I2C_LCD import I2cLcd
from machine import SoftI2C,ADC,Pin,SDCard

DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(14), sda=Pin(13), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("loading ..." )
lcd.move_to(0, 1)
lcd.putstr("loading ..." )

# Slot 2 uses pins sck=18, cs=5, miso=19, mosi=23
sd = SDCard(slot=2)

vfs.mount(sd, '/sd') # mount

interrupt = False

# interval of measurements in seconds 120 = 2 minutes
inerval = 120

temperature = 0
humidity = 0
line=''

file = '/sd/test.txt'

try:
    d = dht.DHT11(Pin(4))
    while(not interrupt):
        try:
            d.measure()
            temperature = d.temperature() # eg. 23.6 (°C)
            humidity = d.humidity()    # eg. 41.3 (% RH)
            line = 'T:' + str(temperature) + 'C | H:' + str(humidity)+'%'
            
            sleep_ms(500)
            
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr(line)
            lcd.move_to(0,1)
            lcd.putstr("writing SD")
            sleep_ms(500)
            
            # if file exists, append 
            if os.stat(file)[6] > 0:
                with open(file, 'a') as f:
                    f.write(line+'\n')
                    f.close()
            else:
                with open(file, 'w') as f:
                    f.write(line+'\n')
                    f.close()
                    
            lcd.move_to(0,1)
            lcd.putstr("SD writed     ")
            
            sleep(inerval)
            
        except Exception as e:
            print('error',e)
            sleep_ms(1000)
        except KeyboardInterrupt:
            print('info keyboard interrupt')
            interrupt = True

except Exception as e:
    interrupt = True
    
    lcd.move_to(0,0)
    lcd.putstr(str(e))
    lcd.move_to(0,1)
    lcd.putstr("writing SD")
    
    with open('/sd/test.txt', 'a') as f:
        f.write(str(e))
        f.close()    # close file
    
    lcd.move_to(0,1)
    lcd.putstr("SD writed    ")
    
finally:

    vfs.umount('/sd')    # eject