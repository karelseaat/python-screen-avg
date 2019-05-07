from message import message

class mesgType(object):

    mesg = None

    def __init__(self):
        self.mesg = message()
        self.type = [self.type_receve_lightar, self.type_receve_config, self.type_receve_register]
        self.functref = {}

    def shownrofmesg(self):
        return len(self.type)

    def addfunctonum(self, funct, num):
        self.functref[num] = funct

    def type_send_lightar(self, lightar):
        toret = self.mesg.pack_short_int(0) + self.mesg.pack_color_ar(lightar)
        return toret

    def type_send_config(self, config):
        toret = self.mesg.pack_short_int(1) + self.mesg.pack_float(config['saturation']) + self.mesg.pack_short_int(config['brightness'])
        return toret

    def type_send_register(self):
        return self.mesg.pack_short_int(2)

    def type_receve_lightar(self):
        return self.mesg.unpack_color_ar()

    def type_receve_config(self):
        toret = {'saturation':self.mesg.unpack_float(), 'brightness':self.mesg.unpack_short_int()}
        return toret

    def type_receve_register(self):
        return True

    def decodetype(self, mesg, addr):
        self.mesg.discard()
        self.mesg.add(mesg)
        mestype = self.mesg.unpack_short_int()

        if mestype in self.functref:
            self.functref[mestype](mesg, addr)
