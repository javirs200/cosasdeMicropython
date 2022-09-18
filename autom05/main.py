from myservo import myServo
from hcsr04 import SR04
import time

SR=SR04(13,14)

servoth=myServo(25)
servoth.myServoWriteAngle(90)

servost=myServo(27)
servost.myServoWriteAngle(90)

time.sleep_ms(2000)

try:
    while True:
        time.sleep_ms(500)
        servost.myServoWriteAngle(40)
        time.sleep_ms(500)
        servost.myServoWriteAngle(90)
        time.sleep_ms(500)
        servost.myServoWriteAngle(140)
        time.sleep_ms(500)
        servost.myServoWriteAngle(90)
        time.sleep_ms(500)
        print('Distance: ',SR.distance(),'cm')
        time.sleep_ms(500)
        servoth.myServoWriteAngle(90)
        time.sleep_ms(500)
        servoth.myServoWriteAngle(100)
        time.sleep_ms(500)
        servoth.myServoWriteAngle(90)
        time.sleep_ms(500)
        servoth.myServoWriteAngle(80)
        time.sleep_ms(500)
        servoth.myServoWriteAngle(90)
        time.sleep_ms(500)

except KeyboardInterrupt:
        print('Interrupted')
        servoth.deinit()
        servost.deinit()
except:
    servoth.deinit()
    servost.deinit()


