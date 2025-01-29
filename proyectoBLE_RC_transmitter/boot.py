# MicroPython Human Interface Device library
# Copyright (C) 2021 H. Groefsema
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Implements a BLE HID joystick
import utime
import uasyncio as asyncio
from machine import Pin 
from hid_services import Joystick

class Device:

    def handler_x(self,pin):
        #if rising edge start timer
        if self.pin_x.value() == 1:
            self.start_x = utime.ticks_us()
        #if falling edge stop timer and calculate pwm
        else:
            self.end_x = utime.ticks_us()
            self.pwm_x = utime.ticks_diff(self.end_x, self.start_x)

            if 900 < self.pwm_x < 2500:
                if self.pwm_x > self.max_pwm_x:
                    self.max_pwm_x = self.pwm_x
                if self.pwm_x < self.min_pwm_x:
                    self.min_pwm_x = self.pwm_x

            


    def handler_y(self,pin):
        #if rising edge start timer
        if self.pin_y.value() == 1:
            self.start_y = utime.ticks_us()
        #if falling edge stop timer and calculate pwm
        else:
            self.end_y = utime.ticks_us()
            self.pwm_y = utime.ticks_diff(self.end_y, self.start_y)

            if 900 < self.pwm_y < 2500:
                if self.pwm_y > self.max_pwm_y:
                    self.max_pwm_y = self.pwm_y
                if self.pwm_y < self.min_pwm_y:
                    self.min_pwm_y = self.pwm_y
    
    def remap(self, v, oMin, oMax, nMin, nMax ):

        NewValue = int((((v - oMin) * (nMax - nMin)) / (oMax - oMin)) + nMin)

        return NewValue


    def __init__(self, name="Joystick"):
        # Define state
        self.axes = (0, 0)
        self.updated = False
        self.active = True

        # Define pin axes as interupts
        self.pin_x = Pin(32, Pin.IN)
        self.pin_y = Pin(33, Pin.IN)

        self.pin_x.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.handler_x)
        self.pin_y.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.handler_y)

        # Define pwm values
        self.pwm_x = 0
        self.pwm_y = 0

        # Define start and end time
        self.start_x = 0
        self.end_x = 0
        self.start_y = 0
        self.end_y = 0

        # define actual pwm limit values
        self.max_pwm_x = 2000
        self.min_pwm_x = 1500

        self.max_pwm_y = 2000
        self.min_pwm_y = 1500

        # Create our device
        self.joystick = Joystick(name)
        # Set a callback function to catch changes of device state
        self.joystick.set_state_change_callback(self.joystick_state_callback)

    # Function that catches device status events
    def joystick_state_callback(self):
        if self.joystick.get_state() is Joystick.DEVICE_IDLE:
            return
        elif self.joystick.get_state() is Joystick.DEVICE_ADVERTISING:
            return
        elif self.joystick.get_state() is Joystick.DEVICE_CONNECTED:
            return
        else:
            return

    def advertise(self):
        self.joystick.start_advertising()

    def stop_advertise(self):
        self.joystick.stop_advertising()

    async def advertise_for(self, seconds=30):
        self.advertise()

        while seconds > 0 and self.joystick.get_state() is Joystick.DEVICE_ADVERTISING:
            await asyncio.sleep(1)
            seconds -= 1

        if self.joystick.get_state() is Joystick.DEVICE_ADVERTISING:
            self.stop_advertise()

    # Input loop
    async def gather_input(self):
        while self.active:
            prevaxes = self.axes

            # map the pwm values to the range of -127 to 127
            self.axes = (self.remap(self.pwm_x, self.min_pwm_x, self.max_pwm_x, -127, 127)
                         , self.remap(self.pwm_y, self.min_pwm_y, self.max_pwm_y, -127, 127))
            # debug log
            # print(self.axes, self.pwm_x, self.pwm_y, self.min_pwm_x, self.max_pwm_x, self.min_pwm_y, self.max_pwm_y)
            self.updated = self.updated or not (prevaxes == self.axes)  # If updated is still True, we haven't notified yet
            await asyncio.sleep_ms(50)

    # Bluetooth device loop
    async def notify(self):
        while self.active:
            # If connected, set axes and notify
            # If idle, start advertising for 30s or until connected
            if self.updated:
                if self.joystick.get_state() is Joystick.DEVICE_CONNECTED:
                    self.joystick.set_axes(self.axes[0], self.axes[1])
                    self.joystick.notify_hid_report()
                elif self.joystick.get_state() is Joystick.DEVICE_IDLE:
                    await self.advertise_for(30)
                self.updated = False

            if self.joystick.get_state() is Joystick.DEVICE_CONNECTED:
                await asyncio.sleep_ms(50)
            else:
                await asyncio.sleep(2)

    async def co_start(self):
        # Start our device
        if self.joystick.get_state() is Joystick.DEVICE_STOPPED:
            self.joystick.start()
            self.active = True
            await asyncio.gather(self.advertise_for(30), self.gather_input(), self.notify())

    async def co_stop(self):
        self.active = False
        self.joystick.stop()

    def start(self):
        asyncio.run(self.co_start())

    def stop(self):
        asyncio.run(self.co_stop())

    # Test routine
    async def test(self):
        while not self.joystick.is_connected():
            await asyncio.sleep(5)

        await asyncio.sleep(5)
        self.joystick.set_battery_level(50)
        self.joystick.notify_battery_level()
        await asyncio.sleep_ms(500)

        for i in range(30):
            self.joystick.set_axes(100,100)
            self.joystick.set_buttons(1)
            self.joystick.notify_hid_report()
            await asyncio.sleep_ms(500)

            self.joystick.set_axes(100,-100)
            self.joystick.set_buttons(b3=1)
            self.joystick.notify_hid_report()
            await asyncio.sleep_ms(500)

            self.joystick.set_axes(-100,-100)
            self.joystick.set_buttons()
            self.joystick.notify_hid_report()
            await asyncio.sleep_ms(500)

            self.joystick.set_axes(-100,100)
            self.joystick.set_buttons(b2=1)
            self.joystick.notify_hid_report()
            await asyncio.sleep_ms(500)

        self.joystick.set_axes(0,0)
        self.joystick.set_buttons()
        self.joystick.notify_hid_report()
        await asyncio.sleep_ms(500)

        self.joystick.set_battery_level(100)
        self.joystick.notify_battery_level()

    async def co_start_test(self):
        self.joystick.start()
        await asyncio.gather(self.advertise_for(30), self.test())

    # start test
    def start_test(self):
        asyncio.run(self.co_start_test())

if __name__ == "__main__":
    d = Device()
    d.start()
