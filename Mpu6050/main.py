from mpu6050 import MPU6050
import time
 
mpu=MPU6050(14,13) #attach the IIC pin(sclpin,sdapin)
mpu.MPU_Init()     #initialize the MPU6050
time.sleep_ms(1000)#waiting for MPU6050 to work steadily

gx = 0.0
gy = 0.0
gz = 0.0

try:
    while True:
        gyro=mpu.MPU_Get_Gyroscope()     #gain the values of Gyroscope
        dsx = gyro[0]/131
        dsy = gyro[1]/131
        dsz = gyro[2]/131
        gx = gx + dsx
        gy = gy + dsy
        gz = gz + dsz
        print(dsx," dsx ",dsy," dsy ",dsz," dsz ")
        print(gx," gx ",gy," gy ",gz," gz ")
        time.sleep_ms(1000)
        pass
except:
    pass