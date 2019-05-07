# -*- coding: utf-8 -*-
# Based on https://github.com/JanBednarik/micropython-ws2812
# Adapted for LoPy by @aureleq

import gc
from machine import SPI
from machine import Pin
from machine import disable_irq
from machine import enable_irq
from uos import uname

class ws2812:

    # Values to put inside SPi register for each color's bit
    buf_bytes = (0xE0E0, 0xFCE0, 0xE0FC, 0xFCFC)

    def __init__(self, ledNumber=1, brightness=100, dataPin=2):
        """
        Params:
        * ledNumber = count of LEDs
        * brightness = light brightness (integer : 0 to 100%)
        * dataPin = pin to connect data channel (LoPy only)
        """
        self.ledNumber = ledNumber
        self.brightness = brightness

        # Prepare SPI data buffer (8 bytes for each color)
        self.buf_length = self.ledNumber * 3 * 8
        self.buf = bytearray(self.buf_length)

        # SPI init
        self.spi = SPI(1, baudrate=8000000, polarity=0, phase=1, sck=Pin(0), mosi=Pin(dataPin), miso=Pin(0))
        # Enable pull down
        Pin(dataPin, mode=Pin.OUT, pull=Pin.PULL_DOWN)

        # Turn LEDs off
        self.show([])

    def show(self, data):
        self.fill_buf(data)
        self.send_buf()

    def send_buf(self):
        disable_irq()
        self.spi.write(self.buf)
        enable_irq()
        gc.collect()

    def update_buf(self, data, start=0):

        buf = self.buf
        buf_bytes = self.buf_bytes
        brightness = self.brightness

        index = start * 24
        for red, green, blue in data:
            red = int(red * brightness // 100)
            green = int(green * brightness // 100)
            blue = int(blue * brightness // 100)

            buf[index] = buf_bytes[green >> 6 & 0x03]
            buf[index+2] = buf_bytes[green >> 4 & 0x03]
            buf[index+4] = buf_bytes[green >> 2 & 0x03]
            buf[index+6] = buf_bytes[green & 0x03]

            buf[index+8] = buf_bytes[red >> 6 & 0x03]
            buf[index+10] = buf_bytes[red >> 4 & 0x03]
            buf[index+12] = buf_bytes[red >> 2 & 0x03]
            buf[index+14] = buf_bytes[red & 0x03]

            buf[index+16] = buf_bytes[blue >> 6 & 0x03]
            buf[index+18] = buf_bytes[blue >> 4 & 0x03]
            buf[index+20] = buf_bytes[blue >> 2 & 0x03]
            buf[index+22] = buf_bytes[blue & 0x03]

            index += 24

        return index // 24

    def fill_buf(self, data):
        end = self.update_buf(data)
        buf = self.buf
        off = self.buf_bytes[0]
        for index in range(end * 24, self.buf_length):
            buf[index] = off
            index += 2

    def set_brightness(self, brightness):
        self.brightness = brightness
