#!/usr/bin/env python 

from uuid import uuid4
from twisted.application import internet, service
from twisted.internet.protocol import DatagramProtocol
from twisted.python import log

from Xlib import display, X
from PIL import Image
from struct import *
import zlib
import time
from yaml import load, dump

class PingPongProtocol(DatagramProtocol):
    # de ping pong classe moet worden aangepast, die naam kan niet meer
    noisy = False

    def __init__(self, controller, port):
        self.port = port
        self.settings = load(open("settings.yml", 'r'))
        self.clients = {}

    def hasclients(self):
        return bool(self.clients)

    def packcolors(self, colors):
        string = pack("B", len(colors)/3)
        string += colors
        return string

    def sendColors(self,colors):
        
        todel = None

        for key, val in self.clients.iteritems():
            # hier gaan we net zo goed de pack colors sturen, maar deze keer doen we er een ident bij van wat voorn soort pak het is
            self.transport.write(self.packcolors(colors), key)
            self.clients[key] -= 1
            if val <= 0:
                todel = key

        if todel:
            del self.clients[todel]

    def datagramReceived(self, datagram, addr):
        if datagram.strip() == "register":
            
            if addr not in self.clients:
                # self.transport.write('lol',addr) hier gaan we de config sturen ! met ook hier een iden over wat voorn soort pak het is
                self.clients.update({addr:30})
            else:
                self.clients[addr] = 30


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

        dsp = display.Display()
        self.root = dsp.screen().root
        self.geom = self.root.get_geometry()
        self.steps = (int(self.geom.width/self.W),int(self.geom.height/self.H))


    def getcolors(self):
        colors = b""

        for y in xrange(1,self.steps[1]):
            colors += self.root.get_image(10, (self.steps[1]-y)*self.H, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]

        for x in xrange(1,self.steps[0]):
            colors += self.root.get_image(x*self.W, 10, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]

        for y in xrange(1,self.steps[1]):
            colors += self.root.get_image(self.geom.width-10, y*self.H, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]

        return colors


    def update_colors(self, proto):

        self.start = time.time()
        self.counter += 1

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
            log.msg(self.updatespeed , (self.start - self.end))


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

        proto = PingPongProtocol(controller=self, port=5544)
        root.addService(internet.UDPServer(5544, proto))
        root.addService(internet.TimerService(0.05, self.update_colors, proto))

        return application


application = Broadcaster().makeService()
