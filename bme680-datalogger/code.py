# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# Extended by Scott Candey for ASSURE 2022 at UCB SSL

"""
Data logging example for Pico + bme680. Logs the values to a file on the Pico.
"""
import time
import digitalio
import board
import adafruit_bme680

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

sensor.seaLevelhPa = 1014.8
temperature_offset = -5

starttime = time.monotonic()

try:
    with open("/airmeasures.csv", "a") as datalog:
        while True:
            
            timestamp = time.monotonic() - starttime
            
            temperature = sensor.temperature + temperature_offset
            gas_resistance = sensor.gas
            humidity = sensor.humidity
            pressure = sensor.pressure
            altitude = sensor.altitude

            print('Temperature: {} degrees C'.format(temperature))
            print('Gas: {} ohms'.format(gas_resistance))
            print('Humidity: {}%'.format(humidity))
            print('Pressure: {}hPa'.format(pressure))
            print('Altitude: {} meters'.format(altitude))

            datalog.write(f'{timestamp},{temperature},{gas_resistance},{humidity},{pressure},{altitude}\n')
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