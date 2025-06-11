# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
boot.py file for Pico data logging example. If this file is present when
the pico starts up + , make the filesystem writeable by CircuitPython.
"""
import storage
import board
import digitalio
    
write_pin = digitalio.DigitalInOut(board.A0)
write_pin.direction = digitalio.Direction.INPUT
write_pin.pull = digitalio.Pull.UP

# Setup sytem to be default write mode 
if write_pin.value: # if tied to ground on startup, go into read mode to transfer data 
    storage.remount("/", readonly=False)