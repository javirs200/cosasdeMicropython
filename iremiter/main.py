from machine import Pin
from ir_tx.nec import NEC
from time import sleep

tx = Pin(23, Pin.OUT, value = 0)
sleep(1)
nec = NEC(tx)
print("transmiting nec protocol")
sleep(1)

try:
    while(True):
        nec.transmit(1,268,1)
        sleep(0.2)
except:
    print("exception")