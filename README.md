# RP2040 Testing for ASSURE 2022

## Goals

- To measure temperature and write data to internal flash
- Eventually, to use accelerometer + gyro to measure movement and save to internal flash


## CircuitPython

<https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython>

<https://circuitpython.org/board/adafruit_feather_rp2040/>

### RP2040 instructions
(From Adafruit install page)

You'll want to find two buttons on the RP2040 boards: reset and BOOTSEL/BOOT. The two buttons are the same size - small black buttons. Reset is typically labeled RESET or RST on the board. The boot button is labeled BOOTSEL or BOOT on the board.

To enter the bootloader on an RP2040 board, you must hold down the boot select button, and while continuing to hold it, press and release the reset button. Continue to hold the boot select button until the bootloader drive appears.

Once successful, the RGB status LED(s) on the board will flash red and then stay ~~green~~ red. A new drive will show up on your computer. The drive will be called RPI-RP2 on all RP2040 boards.
