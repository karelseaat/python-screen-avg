
import sys
if sys.platform == 'esp32' or sys.platform == 'esp8266':
    import ustruct as struct
else:
    import struct

class message():
    buff = b""
    pos = 0

    def __len__(self):
        """ get the length of buffer """
        return len(self.buff) - self.pos

    def add(self, data):
        """ add raw data to the buffer """
        self.buff += data

    def save(self):
        self.buff = self.buff[self.pos:]
        self.pos = 0

    def restore(self):
        self.pos = 0

    def discard(self):
        """ empty the buffer """
        self.pos = 0
        self.buff = b""

    def read(self, length=None):
        """ read the buffer and set the pointer where you stopped reading"""
        if length is None:
            data = self.buff[self.pos:]
            self.pos = len(self.buff)
        else:
            if self.pos + length > len(self.buff):
                raise BufferUnderrun()

            data = self.buff[self.pos:self.pos+length]
            self.pos += length

        return data


    def unpack(self, fmt):
        fmt = ">"+fmt
        length = struct.calcsize(fmt)
        fields = struct.unpack(fmt, self.read(length))
        if len(fields) == 1:
            fields = fields[0]
        return fields

    def pack(self, fmt, *fields):
        """ pack but make sure it is big endian """
        return struct.pack(">"+fmt, *fields)

    def unpack_short_int(self):
        """ unpack a byte as a shortint """
        return self.unpack('B')

    def pack_short_int(self, num):
        """ pack a shortint as a byte """
        return self.pack("B", num)

    def pack_float(self, num):
        """ pack a float """
        return self.pack("f", num)

    def unpack_float(self):
        """ unpack a float """
        return self.unpack('f')

    def unpack_color(self):
        """ unpack a color as 3 byes """
        return self.unpack('BBB')

    def pack_color(self, color):
        """ pack a color as 3 bytes """
        return self.pack("BBB", color[0],color[1],color[2])

    def pack_color_ar(self, array):
        bytes = self.pack_short_int(round(len(array)/3))
        return bytes + array

    def unpack_color_ar(self):
        temppix = []
        length = self.unpack_short_int()
        for _ in range(length):
            temppix.append(self.unpack_color())
        return temppix
