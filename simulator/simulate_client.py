#!/usr/bin/env python

import socket
import time
import math
import sys
import os
import tneopixel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../lib")))

from mesg_type import MesgType

def brightness(cols, change):
    """the right way to change brightness acoring to fumulas and shite"""
    if change <= 0:
        change = (change*-1)+0000.1
    elif change >= 1:
        change = 1/change

    # there should be a per color difference in the change since humans
    # eyes and brains, it shall be later.

    return int(cols[0]*change), int(cols[1]*change), int(cols[2]*change)

def saturation(cols, change):
    """change the saturation of the color, dont know how or where,
    perhaps later this will change"""
    compound = colorsqrt(cols)

    red = compound+((cols[0])-compound)*change
    green = compound+((cols[1])-compound)*change
    blue = compound+((cols[2])-compound)*change

    return (red, green, blue)

def normalisation(cols):
    """the normalisation of color"""
    mins = min(cols[0], cols[1], cols[2])
    if mins < 0:
        cols = (cols[0]+(-1*mins), cols[1]+(-1*mins), cols[2]+(-1*mins))

    sums = (cols[0]) + (cols[1]) + (cols[2]) + 1
    red = cols[0]/sums*255
    green = cols[1]/sums*255
    blue = cols[2]/sums*255

    return(red, green, blue)

def colorsqrt(cols):
    """the square rood of color value"""
    return math.sqrt(
        (cols[0]*cols[0]) + (cols[1]*cols[1]) + (cols[2]*cols[2])
    )


def dim_colors(colors, dim):
    """ this will take the color and substact points of every rgb color channel
        and return that color
        this will be done do slowly dimm the color
    """
    color1 = 0 if (colors[0] - dim[0]) < 0 else colors[0] -  dim[0]
    color2 = 0 if (colors[1] - dim[1]) < 0 else colors[1] -  dim[1]
    color3 = 0 if (colors[2] - dim[2]) < 0 else colors[2] -  dim[2]
    return color1, color2, color3



def handleincomingpixels(mesg, addr):
    """ the function to handle incoming pixels message"""
    global pixels
    pixels = mesg.unpack_color_ar()

def handleincomingconfig(mesg, addr):
    """ the function to handle incoming config """
    global lightconfig
    lightconfig = mesg


def clientmode():
    """ the main function """

    global lightconfig, pixels

    lightconfig = {'saturation':0, 'brightness': 0}

    msgtype = MesgType()

    msgtype.addfunctonum(handleincomingpixels, 0)
    msgtype.addfunctonum(handleincomingconfig, 1)

    # neo_pixel = NeoPixel(Pin(2), 90)
    neo_pixel = tneopixel.tneopixel(40)

    multip = "255.255.255.255"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.sendto(msgtype.type_send_register(),(multip, 5544))


    while True:

        try:
            data, addr = client_socket.recvfrom(1024)
            msgtype.decodetype(data, addr)

        except Exception as error:
            print("network udp socket: " + str(error))
            client_socket.sendto(msgtype.type_send_register(),(multip, 5544))
            time.sleep(0.01)

        acount = 0


        while pixels and acount < neo_pixel.n and acount < len(pixels) :

            neo_pixel[acount] = pixels[acount]
            acount += 1
        neo_pixel.write()

clientmode()
