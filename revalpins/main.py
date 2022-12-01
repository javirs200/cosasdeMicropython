import machine, os
#sd_clk=14 sd_data2=12 sd_data3=13 sd_cmd=15 sd_data0=2 sd_data1=4
sd = machine.SDCard(slot=3)

os.mount(sd, '/sd')  # mount

lista = os.listdir('/sd')

for i in lista:
    print(i)

file_name = "/sd/d1.txt"
    
with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        print(data)
 
os.umount('/sd')     # eject