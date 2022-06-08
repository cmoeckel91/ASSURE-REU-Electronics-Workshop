# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# Extended by Scott Candey for ASSURE 2022 at UCB SSL

"""
Data logging example for Pico + bme680. Logs the values to a file on the Pico.
"""
import time
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

import board
import adafruit_bme680
i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

sensor.seaLevelhPa = 1014.8

starttime = time.monotonic()

try:
    with open("/airmeasures.csv", "a") as datalog:
        while True:
            
            timestamp = time.monotonic() - starttime

            print('Temperature: {} degrees C'.format(sensor.temperature))
            print('Gas: {} ohms'.format(sensor.gas))
            print('Humidity: {}%'.format(sensor.humidity))
            print('Pressure: {}hPa'.format(sensor.pressure))
            print('Altitude: {} meters'.format(sensor.altitude))

            datalog.write(f'{timestamp},{sensor.temperature},{sensor.gas},{sensor.humidity},{sensor.pressure},{sensor.altitude}\n')
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