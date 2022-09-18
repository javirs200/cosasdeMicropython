import random
from I2C_LCD import I2cLcd
from machine import SoftI2C,ADC,Pin
import neopixel
import time

def iluminateNeopixel(ci):
    for j in range(0,8):
        np[j]=colors[ci]
        np.write()
        
def ilumniaterainbow():
    for j in range(0,8):
        np[j]=colors[(j%3)]
        np.write()
        
def ilumniategood():
    for j in range(0,4):
        np[j*2]=colors[1]
        np.write()
        
def iluminatebad():
    for j in range(0,4):
        np[j*2]=colors[0]
        np.write()
    

def debugToLCD(adcVal):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("adc : " + str(adcVal) )
    pass



def clasifyAdcVal(adcVal):
    if adcVal < 500 :
        ci=0
    elif adcVal < 800 :
        ci=2
    elif adcVal < 1800 :
        ci=3
    elif adcVal < 2000 :
        ci=1
    return ci



def increaseLevel(secuence:list,level : int):

    secuence.append(random.randint(0,3))
    level += 1

    return secuence,level



def displaySecuence(secuence):

    for ci in secuence:
        iluminateNeopixel(ci)
        time.sleep(0.5)
        iluminateNeopixel(4)
        time.sleep(1)
    pass



def registerInput(secuence):

    termina = False
    for i in secuence:

        adcVal = 0
        while not adcVal:
            adcVal = adc.read()

        ci = clasifyAdcVal(adcVal)
        iluminateNeopixel(ci)
        time.sleep(0.5)
        iluminateNeopixel(4)
        time.sleep(0.5)
        
        #print("ci = " + str(ci) +", i = " + str(i))

        if ci != i :
            iluminatebad()
            time.sleep(0.5)
            return True
        
        pass

    return termina



def printResultLCD(Level):

    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("!! GAME OVER !! " )
    lcd.move_to(0, 1)
    lcd.putstr("Score : " + str(Level) )

    pass



#=====================================init==================================
def init():
    pin = Pin(2, Pin.OUT)
    global np
    np = neopixel.NeoPixel(pin, 8)

    #brightness :0-255
    brightness=10    
    global colors
    colors=[[brightness,0,0],                    #red
            [0,brightness,0],                    #green
            [0,0,brightness],                    #blue
            [brightness,brightness,0],           #yellow
            [0,0,0]]                             #close

    global adc
    adc=ADC(Pin(36))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)

    DEFAULT_I2C_ADDR = 0x27
    i2c = SoftI2C(scl=Pin(14), sda=Pin(13), freq=400000)
    global lcd
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

    gameover = False
    level = 1
    secuence = [random.randint(0, 3)]
    return gameover,level,secuence

#==============================main===============================
def main():
      
    try:
        
        while True :

            gameover, level, secuence = init()

            iluminateNeopixel(4)
            time.sleep(1)
            ilumniaterainbow()

            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Simon Say !!")
            lcd.move_to(0, 1)
            lcd.putstr("press to play")

            adcVal = 0
            while not adcVal:
                adcVal = adc.read()

            iluminateNeopixel(4)
            time.sleep(1)  

            playGame(gameover, level, secuence)

            time.sleep(3)

            pass


        
    except:
        # end except
        pass
    # end main
    pass

def playGame(gameover, level, secuence):
    while not gameover:
            #print("secuencia antes = " + str(secuence) + " level "+  str(level))
        displaySecuence(secuence)

        gameover = registerInput(secuence)

        if not gameover :
            secuence,level = increaseLevel(secuence,level)
            ilumniategood()
            time.sleep(0.5)
            iluminateNeopixel(4)
            time.sleep(1)
                
                #print("secuencia despues = " + str(secuence)  + " level "+  str(level))

    
            # end while
        pass
        
    printResultLCD(level-1)

if __name__ == "__main__":

    main()
    
