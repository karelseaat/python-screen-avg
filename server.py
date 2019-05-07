#!/usr/bin/env python

# from uuid import uuid4
from twisted.application import internet, service
from twisted.internet.protocol import DatagramProtocol
from twisted.python import log

from Xlib import display, X
# from PIL import Image
from struct import *
import zlib
import time
from yaml import load, dump
import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from lib.mesgType import mesgType
from lib.message import message

class PingPongProtocol(DatagramProtocol):
    # de ping pong classe moet worden aangepast, die naam kan niet meer
    # noisy = False

    def __init__(self, controller, port, settings):
        self.port = port
        self.mesgtypes = mesgType()
        self.clients = {}
        self.settings = settings
        self.message = message()

        self.mesgtypes.addfunctonum(self.handleregister, 2)

    def hasclients(self):
        return bool(self.clients)


    def handleregister(self, mesg, addr):
        if addr not in self.clients:
            self.clients.update({addr:30})
        else:
            somemesg = self.mesgtypes.type_send_config(self.settings)
            self.transport.write(somemesg, addr)
            self.clients[addr] = 30

    def sendColors(self,colors):

        todel = None

        for client, val in self.clients.iteritems():
            # hier gaan we net zo goed de pack colors sturen, maar deze keer doen we er een ident bij van wat voorn soort pak het is
            somemesg = self.mesgtypes.type_send_lightar(colors)
            self.transport.write(somemesg, client)
            self.clients[client] -= 1
            if val <= 0:
                todel = client

        if todel:
            del self.clients[todel]

    def datagramReceived(self, datagram, addr):

        self.mesgtypes.decodetype(datagram, addr)




class Broadcaster(object):

    W,H = 90,90
    dsp = None
    root = None
    geom = None
    steps = 0,0
    lastcrc = 0
    colors = []
    updatespeed = 0.2
    counter = 0
    start = 0
    end = 10

    def __init__(self):
        self.settings = load(open("settings.yml", 'r'))
        dsp = display.Display()
        self.root = dsp.screen().root
        self.geom = self.root.get_geometry()
        self.steps = (int(self.geom.width/self.W),int(self.geom.height/self.H))

    def get_left_pixels(self):
        colors = b""
        if self.settings['stringdirection'] == 'counterclockwize':
            somer = range(1, self.steps[1])
        else:
            somer = range(self.steps[1], 1, -1)
        for y in somer:
            colors += self.root.get_image(10, (self.steps[1]-y)*self.H, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]
        return colors

    def get_top_pixels(self):
        colors = b""
        if self.settings['stringdirection'] == 'counterclockwize':
            somer = range(1, self.steps[0])
        else:
            somer = range(self.steps[0], 1, -1)
        for x in somer:
            colors += self.root.get_image(x*self.W, 10, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]
        return colors

    def get_right_colors(self):
        colors = b""
        if self.settings['stringdirection'] == 'counterclockwize':
            somer = range(1, self.steps[1])
        else:
            somer = range(self.steps[1], 1, -1)
        for y in somer:
            colors += self.root.get_image(self.geom.width-10, y*self.H, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]

        return colors

    def getcolors(self):

        if self.settings['stringdirection'] == 'counterclockwize':
            colors = self.get_left_pixels()
            colors += self.get_top_pixels()
            colors += self.get_right_colors()
        else:
            colors = self.get_right_colors()
            colors += self.get_top_pixels()
            colors += self.get_left_pixels()

        return colors


    def update_colors(self, proto):

        self.start = time.time()
        self.counter += 1
        newcolors = []

        if proto.hasclients() and (self.start - self.end) > self.updatespeed:
            newcolors = self.getcolors()
            if newcolors != self.colors:
                self.colors = newcolors
                self.speedup()
            else:
                self.slowdown()
            proto.sendColors(self.colors)
            self.end = time.time()

        if (self.counter % 100) == 0:
            log.msg("updatespeed:",self.updatespeed, " hasclients:" , proto.hasclients())


    def speedup(self):
        if self.updatespeed > 0.05:
            self.updatespeed -= 0.2

    def slowdown(self):
        if self.updatespeed < 1.5:
            self.updatespeed += 0.2

    def makeService(self):
        application = service.Application('Broadcaster')

        root = service.MultiService()
        root.setServiceParent(application)

        proto = PingPongProtocol(controller=self, port=5544, settings=self.settings)
        root.addService(internet.UDPServer(5544, proto))
        root.addService(internet.TimerService(0.05, self.update_colors, proto))

        return application


application = Broadcaster().makeService()
