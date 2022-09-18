from I2C_LCD import I2cLcd
from machine import SoftI2C,ADC,Pin
import neopixel
import time

def iluminateNeopixel(np, colors, ci):
    for j in range(0,8):
        np[j]=colors[ci]
        np.write()

def debugToLCD(lcd, color, adcVal):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("adc : " + str(adcVal) )
    lcd.move_to(0, 1)
    lcd.putstr("color : " + color )



def clasifyAdcVal(adcVal):
    if adcVal < 500 :
        color = "rojo"
        ci=0
    elif adcVal < 800 :
        color = "azul"
        ci=2
    elif adcVal < 1800 :
       color = "amarillo"
       ci=3
    elif adcVal < 2000 :
        color = "verde"
        ci=1
    return color,ci

def init():
    pin = Pin(2, Pin.OUT)
    np = neopixel.NeoPixel(pin, 8)

    #brightness :0-255
    brightness=10                                
    colors=[[brightness,0,0],                    #red
            [0,brightness,0],                    #green
            [0,0,brightness],                    #blue
            [brightness,brightness,0],  #white
            [0,0,0]]                             #close

    adc=ADC(Pin(36))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)

    DEFAULT_I2C_ADDR = 0x27
    i2c = SoftI2C(scl=Pin(14), sda=Pin(13), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

    gameover = False
    color = ""
    ci=4
    return np,colors,adc,lcd,gameover,ci

#==============================main===============================
def main():
    
    np, colors, adc, lcd, gameover, ci = init()
    
    iluminateNeopixel(np, colors,ci)

    try:
        
        lcd.move_to(0, 0)
        lcd.putstr("Hello,world!")
        
        while not gameover:
            
            adcVal = adc.read()
            
            if adcVal:

                color, ci = clasifyAdcVal(adcVal)
                    
                debugToLCD(lcd, color, adcVal)
            
                iluminateNeopixel(np, colors, ci)

                #end if adcVal
                pass
    
            # end while
            pass
        
    except:
        # end except
        pass
    # end main
    pass

if __name__ == "__main__":

    main()
    
