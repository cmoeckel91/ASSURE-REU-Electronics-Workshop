"""
Data logging example for Pico + bme680 + LSM6DSO32. Logs the values to a file on the Pico.
"""
import time
import digitalio
import board
import neopixel
import adafruit_bme680

from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32 as LSM6DS
from adafruit_lsm6ds import Rate

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c = board.I2C()
sensor1 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

sensor1.seaLevelhPa = 1014.8
temperature_offset = -5

sensor2 = LSM6DS(i2c)
sensor2.accelerometer_data_rate = Rate.RATE_26_HZ
sensor2.gyro_data_rate = Rate.RATE_26_HZ

starttime = time.monotonic()

try:
    with open("/measurements.csv", "a") as datalog:
        while True:
            
            timestamp = time.monotonic() - starttime
            
            temperature = sensor1.temperature + temperature_offset
            gas_resistance = sensor1.gas
            humidity = sensor1.humidity
            pressure = sensor1.pressure
            altitude = sensor1.altitude

            acc_x, acc_y, acc_z = sensor2.acceleration
            gyro_x, gyro_y, gyro_z = sensor2.gyro

            dataline = f'{timestamp},{temperature},{gas_resistance},{humidity},{pressure},{altitude},{acc_x},{acc_y},{acc_z},{gyro_x},{gyro_y},{gyro_z}\n'
            print(f'Time {timestamp}, Temp {temperature}, Gas {gas_resistance}, Humid {humidity}, Altitude {altitude}, AccX {acc_x}, AccY {acc_y}, AccZ {acc_z}, GyroX {gyro_x}, GyroY {gyro_y}, GyroZ {gyro_z}')
            datalog.write(dataline)
            datalog.flush()
            led.value = not led.value
            time.sleep(0.1)

except OSError as e:  # Typically when the filesystem isn't writeable...
    print(f'OSError {e}')
    pixels.fill((255, 0, 0))
    delay = 1  # ...blink the LED every half second.
    if e.args[0] == 28:  # If the filesystem is full...
        delay = 0.5  # ...blink the LED faster!
    while True:
        led.value = not led.value
        time.sleep(delay)