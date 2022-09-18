import network
import socket
import time
from myservo import myServo

ssidRouter     =  "HUAWEI P30 lite"       #Enter the router name
passwordRouter =  "xcom1234"       #Enter the router password
port           =   8000            #input the remote port
wlan=None
listenSocket=None

servo=myServo(15)
servo.myServoWriteAngle(90)
servo.driveMotor(True,0)

def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
    print("searching preconfigured wifi network")
  return True

def rangeconv(OldValue:int,OldMin:int,OldMax:int,NewMin:int,NewMax:int):
  NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
  return NewValue
    
try:
  connectWifi(ssidRouter,passwordRouter)
  ip=wlan.ifconfig()[0]
  listenSocket = socket.socket()
  listenSocket.bind((ip,port))
  listenSocket.listen(1)
  listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  print ('tcp waiting...')
  while True:
    print("Server IP:",ip,"\tPort:",port)
    print("accepting.....")
    conn,addr = listenSocket.accept()
    print(addr,"connected")
    break
  conn.send('I am Server')
  while True:
    data = conn.recv(6)
    if(len(data) == 0):
      print("close socket")
      listenSocket.close()
      wlan.disconnect()
      wlan.active(False)
      break
    else:
      stri = data.decode("utf8")
      if("t:" in stri):
        stri = stri.replace(":", " ")
        stri = stri.replace("\n", "")
        striList = stri.split()
        if(len(striList) > 1):
          #print("len -> " + str(len(striList)))
          if (striList[1].isdigit()):
            #print("isdigit -> " + striList[1])
            angle = rangeconv(int(striList[1]),0,100,0,180)
            servo.myServoWriteAngle(float(angle))
            #print("ordered " + striList[1] + "% moving servo to "+ str(angle))
      elif("h:" in stri):
        stri = stri.replace(":", " ")
        stri = stri.replace("\n", "")
        striList = stri.split()
        if(len(striList) > 1):
          #print("len -> " + str(len(striList)))
          if (striList[1].isdigit()):
            #print("isdigit -> " + striList[1])
            spd = rangeconv(int(striList[1]),0,100,-1023,1023)
            dire = spd > 0
            servo.driveMotor(dire,int(spd))
            print("ordered " + striList[1] + "% drive motor at spd : "+ str(spd)) 
        else:      
          #print("recived ->" + stri)
          pass
          #echo send
          #ret = conn.send(data)              
except Exception as e:
  print("error " + str(e))
  print("Close TCP-Server, please reset.")
  servo.deinit()
  if(listenSocket):
    listenSocket.close()
  wlan.disconnect()
  wlan.active(False)