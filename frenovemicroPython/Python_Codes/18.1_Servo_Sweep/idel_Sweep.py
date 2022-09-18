from myservo import myServo
import time

servo=myServo(15)
servo.myServoWriteAngle(0)
time.sleep_ms(1000)

try:
    while True:
        time.sleep_ms(1500)
        servo.myServoWriteAngle(0)
        time.sleep_ms(1500)
        servo.myServoWriteAngle(90)
        time.sleep_ms(1500)
        servo.myServoWriteAngle(180)
except KeyboardInterrupt:
        print('Interrupted')
        servo.deinit()
except:
    servo.deinit()