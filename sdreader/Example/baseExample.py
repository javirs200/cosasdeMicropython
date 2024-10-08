import machine, os, vfs
from time import sleep_ms

# Slot 2 uses pins sck=18, cs=5, miso=19, mosi=23
sd = machine.SDCard(slot=2)

vfs.mount(sd, '/sd') # mount

with open('/sd/test.txt', 'w') as f:
    f.write('test')
    F.flush()
    f.close()
    
with open('/sd/test.txt', 'r') as f:
    print(f.read())    # read from file
    f.close()    # close file

vfs.umount('/sd')    # eject