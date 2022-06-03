# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# Extended by Scott Candey for ASSURE 2022 at UCB SSL

"""
Data logging example for Pico. Logs the temperature to a file on the Pico.
"""
import time
import board
import digitalio
import time

from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32 as LSM6DS
from adafruit_lsm6ds import Rate


led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = LSM6DS(i2c)
sensor.accelerometer_data_rate = Rate.RATE_26_HZ
sensor.gyro_data_rate = Rate.RATE_26_HZ

starttime = time.monotonic()

try:
    with open("/positioning.csv", "a") as datalog:
        while True:

            acc_x, acc_y, acc_z = sensor.acceleration
            gyro_x, gyro_y, gyro_z = sensor.gyro
            
            timestamp = time.monotonic() - starttime

            print(f'Seconds: {timestamp} Acceleration (m/s^2) X: {acc_x} Y: {acc_y} Z: {acc_z} Gyro (rad/s) X: {gyro_x} Y: {gyro_y} Z: {gyro_z}')

            datalog.write(f'{timestamp},{acc_x},{acc_y},{acc_z},{gyro_x},{gyro_y},{gyro_z}\n')
            datalog.flush()
            led.value = not led.value
            time.sleep(0.1)

except OSError as e:  # Typically when the filesystem isn't writeable...
    delay = 0.5  # ...blink the LED every half second.
    if e.args[0] == 28:  # If the filesystem is full...
        delay = 0.25  # ...blink the LED faster!
    while True:
        led.value = not led.value
        time.sleep(delay)