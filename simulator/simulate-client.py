import socket
import time
import math
import sys, os
import tneopixel
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../lib")))


def brightness(cols, change):
    """the right way to change brightness acoring to fumulas and shite"""
    if change <= 0:
        change = (change*-1)+0000.1
    elif change >= 1:
        change = 1/change

    # there should be a per color difference in the change since humans eyes and brains, it shall be later.

    return int(cols[0]*change), int(cols[1]*change), int(cols[2]*change)

def saturation(cols, change):
    """chnage the saturation of the color, dont know how or where, perhaps later this will change"""
    p = colorsqrt(cols)

    R=p+((cols[0])-p)*change
    G=p+((cols[1])-p)*change
    B=p+((cols[2])-p)*change

    return (R,G,B)

def normalisation(cols):
    """the normalisation of color"""
    mins = min(cols[0], cols[1], cols[2])
    if mins < 0:
        cols = (cols[0]+(-1*mins), cols[1]+(-1*mins), cols[2]+(-1*mins))

    sums = (cols[0]) + (cols[1]) + (cols[2]) + 1
    r = cols[0]/sums*255
    g = cols[1]/sums*255
    b = cols[2]/sums*255

    return(r,g,b)

def colorsqrt(cols):
    """the square rood of color value"""
    return math.sqrt(
        (cols[0]*cols[0]) + (cols[1]*cols[1]) + (cols[2]*cols[2])
    )


def dimColors(colors, dim):
    """this will take the color and substact points of every rgb color channel and return that color
        this will be done do slowly dimm the color
    """
    color1 = 0 if (colors[0] - dim[0]) < 0 else colors[0] -  dim[0]
    color2 = 0 if (colors[1] - dim[1]) < 0 else colors[1] -  dim[1]
    color3 = 0 if (colors[2] - dim[2]) < 0 else colors[2] -  dim[2]
    return color1, color2, color3

def connection(network_name, network_password):
    """Attempt to connect to accesspoint when you connect return the connection. . . connection is station"""
    attempts = 0
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print("Connecting to network...")
        station.active(True)
        station.connect(network_name, network_password)
        while not station.isconnected():
            print("Attempts: {}".format(attempts))
            attempts += 1
            time.sleep(5)
            if attempts > 3:
                return None
                break
    print('Network Config:', station.ifconfig())
    return station



def handleincomingpixels(mesg, addr):
    pixels = mesg

def handleincomingconfig(mesg, addr):
    lightconfig = mesg


def clientmode():
    from mesgType import mesgType
    
    global pixels, lightconfig

    msgtype = mesgType()

    msgtype.addfunctonum(handleincomingpixels, 0)
    msgtype.addfunctonum(handleincomingconfig, 1)

    # np = NeoPixel(Pin(2), 90)
    np = tneopixel.tneopixel(90)

    multip = "255.255.255.255"
    so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # so.setblocking(False)
    so.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    so.sendto(msgtype.type_send_register(),(multip, 5544))

    timeout = 0

    while True:

        pixels = []
        length = 1

        try:
            timeout = 0
            data,addr = so.recvfrom(1024)
            msgtype.decodetype(data, addr)

        except Exception as e:
            print("network udp socket: " + str(e))

            so.sendto(msgtype.type_send_register(),(multip, 5544))
            time.sleep(0.01)

            if timeout < 8000:
                timeout += 1

            for pix in range(np.n):
                np[pix] = dimColors(np[pix], (int(timeout/32),int(timeout/32),int(timeout/32)))
            np.write()

        incrementer = length / np.n
        acount = 0
        while acount < np.n and pixels:
            np[acount] = brightness(normalisation(saturation(pixels[int(acount*incrementer)],lightconfig['saturation'])),lightconfig['brightness'])
            acount += 1
        np.write()

import socket
clientmode()