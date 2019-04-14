from machine import SPI

class WS2813:

    buf_bytes = (0x88, 0x8e, 0xe8, 0xee)

    def __init__(self, spi_bus, led_count=1, intensity=1):
        self.n = led_count
        self.intensity = intensity
        self.colors = [(0,0,0)] * self.n
        self.buf_length = self.n * 3 * 4
        self.spi = SPI(spi_bus, baudrate=3200000, polarity=0, phase=1)
        self.write()

    def write(self):
        buf = bytearray(self.buf_length)
        mask = 0x03
        index = 0

        for red, green, blue in self.colors:
            red = int(red * self.intensity)
            green = int(green * self.intensity)
            blue = int(blue * self.intensity)

            buf[index] = self.buf_bytes[green >> 6 & mask]
            buf[index+1] = self.buf_bytes[green >> 4 & mask]
            buf[index+2] = self.buf_bytes[green >> 2 & mask]
            buf[index+3] = self.buf_bytes[green & mask]

            buf[index+4] = self.buf_bytes[red >> 6 & mask]
            buf[index+5] = self.buf_bytes[red >> 4 & mask]
            buf[index+6] = self.buf_bytes[red >> 2 & mask]
            buf[index+7] = self.buf_bytes[red & mask]

            buf[index+8] = self.buf_bytes[blue >> 6 & mask]
            buf[index+9] = self.buf_bytes[blue >> 4 & mask]
            buf[index+10] = self.buf_bytes[blue >> 2 & mask]
            buf[index+11] = self.buf_bytes[blue & mask]

            index += 12

        self.spi.write(buf)

    def __setitem__(self, index, val):
        self.colors[index] =  val

    def __getitem__(self, index):
        return self.colors[index]

    def update_buf(self, data):
        self.colors = data

    def fill(self, color):
        self.update_buf( [color] * self.n )
