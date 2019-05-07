
import sys
if sys.platform == 'esp32' or sys.platform == 'esp8266':
    import ustruct as struct
else:
    import struct

class message():
    buff = b""
    pos = 0

    def __len__(self):
        return len(self.buff) - self.pos

    def add(self, data):
        self.buff += data

    def save(self):
        self.buff = self.buff[self.pos:]
        self.pos = 0

    def restore(self):
        self.pos = 0

    def discard(self):
        self.pos = 0
        self.buff = b""

    def read(self, length=None):
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
        return struct.pack(">"+fmt, *fields)

    def unpack_short_int(self, stringonly=False):
        return self.unpack('B')

    def pack_short_int(self, num):
        fmt = "B"
        return self.pack(fmt, num)

    def pack_float(self, num):
        fmt = "f"
        return self.pack(fmt, num)

    def unpack_float(self):
        return self.unpack('f')

    def unpack_color(self, stringonly=False):
        return self.unpack('BBB')

    def pack_color(self, color):
        fmt = "BBB"
        return self.pack(fmt, color[0],color[1],color[2])

    def pack_color_ar(self, array):
        bytes = self.pack_short_int(len(array)/3)
        return bytes + array

    def unpack_color_ar(self):
        temppix = []
        length = self.unpack_short_int()
        for i in range(length):
            temppix.append(self.unpack_color())
        return temppix
