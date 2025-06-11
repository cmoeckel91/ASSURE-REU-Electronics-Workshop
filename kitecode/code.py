"""
Data logging example for Pico + bme680 + LSM6DSO32. Logs the values to a file on the Pico.
"""
import time
import digitalio
import board
import adafruit_bme680

from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32
from adafruit_lsm6ds import Rate, AccelRange, GyroRange

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

i2c = board.STEMMA_I2C()
# i2c = board.I2C()

atmosphere = adafruit_bme680.Adafruit_BME680_I2C(i2c, refresh_rate=100, debug=False)
temperature_offset = -5
atmosphere.sea_level_pressure = 1013.25
# atmosphere.temperature_oversample = 1
# atmosphere.pressure_oversample = 1
# atmosphere.humidity_oversample = 1

accgyro = LSM6DSO32(i2c)
accgyro.accelerometer_data_rate = Rate.RATE_208_HZ
accgyro.accelerometer_range = AccelRange.RANGE_8G
accgyro.gyro_data_rate = Rate.RATE_208_HZ
accgyro.gyro_range = GyroRange.RANGE_250_DPS

starttime = time.monotonic()

can_write = False

acc_per_atmos = 8 # 3 second delay between measures

# get_atmosphere = True

try:
    datalog = open("/measurements.csv", "a") # Creates a new file, when none exists. 
except OSError as e:  # Typically when the filesystem isn't writeable...
    print(f'OSError occured while opening file, presumably flash is not in read/write mode: {e}')
except Exception as e:
    print(f'Unexpected exception occured while opening file: {e}')
else:
    can_write = True


while True:


    temperature = atmosphere.temperature + temperature_offset # in degC
    humidity = atmosphere.humidity # in RH %
    pressure = atmosphere.pressure # in ??
    timestamp = time.monotonic() - starttime
    print(f'Time {timestamp}, Temp {temperature}, Humid {humidity}, Pressure {pressure}')

    #     print(f'Wrote timestamp {timestamp} data to flash')
    # else:
    #     print(f'No data written to flash')


    for i in range(acc_per_atmos):
        acc_x, acc_y, acc_z = accgyro.acceleration
        acc_x, acc_y, acc_z = (acc_x / 2, acc_y / 2, acc_z / 2 ) # fix offset issue
        gyro_x, gyro_y, gyro_z = accgyro.gyro # in rad/s
        timestamp = time.monotonic() - starttime
        print(f'Time {timestamp}, AccX {acc_x}, AccY {acc_y}, AccZ {acc_z}, GyroX {gyro_x}, GyroY {gyro_y}, GyroZ {gyro_z}')

        if can_write:
            datalog.write(f'{timestamp},{temperature},{humidity},{pressure},{acc_x},{acc_y},{acc_z},{gyro_x},{gyro_y},{gyro_z}\n')
            datalog.flush()

        time.sleep(0.5)
        #     print(f'Wrote timestamp {timestamp} data to flash')
        # else:
        #     print(f'No data written to flash')

    led.value = not led.value

    # time.sleep(0.1)
