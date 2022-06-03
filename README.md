# RP2040 Testing for ASSURE 2022

## Goals

[x] To measure temperature and write data to internal flash

[x] Save time relative to startup to flash

[ ] Eventually, to use accelerometer + gyro to measure movement and save to internal flash


## CircuitPython

<https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython>

<https://circuitpython.org/board/adafruit_feather_rp2040/>

### RP2040 setup instructions
(From Adafruit install page)

You'll want to find two buttons on the RP2040 boards: reset and BOOTSEL/BOOT. The two buttons are the same size - small black buttons. Reset is typically labeled RESET or RST on the board. The boot button is labeled BOOTSEL or BOOT on the board.

To enter the bootloader on an RP2040 board, you must hold down the boot select button, and while continuing to hold it, press and release the reset button. Continue to hold the boot select button until the bootloader drive appears.

Once successful, the RGB status LED(s) on the board will flash red and then stay ~~green~~ red. A new drive will show up on your computer. The drive will be called RPI-RP2 on all RP2040 boards.


### RP2040 Write to flash instructions
<https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger>

- Can't use flash access via computer and flash access via code at the same time
- boot.py sets up code access
- remove boot.py with REPL over serial to reset

```
import os; os.remove("boot.py")
```

### Additional libraries
Download all here: <https://circuitpython.org/libraries>

Copy required libraries + their dependencies to the lib directory on the circuitpy volume

## Sensing and saving

### CPU Temperature data logger

- After installing CircuitPy, attach Feather via USB cable
- Copy `boot.py` and `code.py` from `temp-datalogger` to `CIRCUITPY` mounted drive
- Press reset button (mounted drive should disappear)
- When drive remounts, check that it is read-only. (May have limited checking of files, even if they are being written continuously, only a few lines may appear)
- When finished recording data, open serial monitor with `screen /dev/tty.usbmodem14201` for Mac, or Mu software for any OS
- Press CTRL+C (or equivalent) and then press any key to enter REPL
- Run `import os; os.rename('boot.py', 'flash.py')`
- Press reset button to reload default boot
- Check to see that temperature data was recorded as expected


### Accelerometer 
LSM6DS032 

Product: <https://www.adafruit.com/product/4692> 

Tutorial: <https://learn.adafruit.com/lsm6dsox-and-ism330dhc-6-dof-imu>

Library: <https://github.com/adafruit/Adafruit_CircuitPython_LSM6DS>

Library example: <https://github.com/adafruit/Adafruit_CircuitPython_LSM6DS/blob/main/examples/lsm6ds_full_test.py>

Datasheet: <https://www.st.com/resource/en/datasheet/lsm6dso32.pdf>

Depends on:
- CircuitPython
- Bus Device (adafruit_bus_device)
- Register (adafruit_register)


Strangely reads 20m/s^s for gravity instead of 9m/s^2 ???

### Magnetometer
TLV493D 

Product: <https://www.adafruit.com/product/4366>

## Notes

CircuitPy has no interrupts, use the new asyncio implementation to get millisecond-ish timing of tasks. This is probably okay for most any application, with the possible exception of the Once A Second PPS for SWEM. 

PIO is cool
<https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython?view=all>


