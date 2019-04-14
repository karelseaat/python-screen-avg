import ustruct as struct


class type(object):

    def __init(self)__:
        self.mesg = Message()
        self.type = [type_receve_lightar, type_receve_config, type_receve_register]

    def type_send_lightar(self, lightar):
        return self.mesg.pack_short_int(1) + lightar

    def type_send_config(self, config):
        self.mesg.pack_short_int(1) + ???

    def type_send_register(self):
        self.mesg.pack_short_int(3)

    def type_receve_lightar(self):
        return self.mesg.unpack_color_ar()

    def type_receve_config(self):
        self.mesg

    def type_receve_register(self):
        self.mesg

    def decodetype(self, mesg):
        self.mesg.add(mesg)
        mestype = self.mesg.unpack_short_int()
        return self.type[mestype]()



class Message(object):
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

    def unpack_color(self, stringonly=False):
        return self.unpack('BBB')

    def pack_color(self, color):
        fmt = "BBB"
        return self.pack(fmt, color[0],color[1],color[2])

    def pack_color_ar(self, array):
        pass

    def unpack_color_ar(self):
        temppix = []
        length = self.unpack_short_int()
        for i in range(length):
            temppix.append(mes.unpack_color())
        return temppix