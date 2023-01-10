
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../lib")))

from message import message

class MesgType():

    mesg = None

    def __init__(self):
        self.mesg = message()
        self.functref = {}

    def addfunctonum(self, funct, num):
        """ add a function to handeling receving data
        indicated by type id = num """

        self.functref[num] = funct

    def type_send_lightar(self, lightar):
        """ send lightar message with id 0 """
        toret = self.mesg.pack_short_int(0) + self.mesg.pack_color_ar(lightar)
        return toret

    def type_send_config(self, config):
        """ send config message with id 1 """
        toret = (
            self.mesg.pack_short_int(1)+
            self.mesg.pack_float(config['saturation'])+
            self.mesg.pack_short_int(config['brightness'])
        )
        return toret

    def type_send_register(self):
        """ send register message with id 2 """
        return self.mesg.pack_short_int(2)

    def decodetype(self, mesg, addr):
        """ handeling incoming data and refering to a handeling function,
        that is registred """
        self.mesg.discard()
        self.mesg.add(mesg)
        mestype = self.mesg.unpack_short_int()

        if mestype in self.functref:
            self.functref[mestype](self.mesg, addr)
