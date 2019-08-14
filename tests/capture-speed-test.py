#!/usr/bin/env python 

from Xlib import display, X
from PIL import Image
import time
from struct import *
from mss import mss

startprog = time.time()

W,H = 90,90
dsp = display.Display()
root = dsp.screen().root
geom = root.get_geometry()
steps = (int(geom.width/W),int(geom.height/H))

def packcolors(colors):
    string = b""
    string = pack("B", len(colors))
    for color in colors:
        string += pack("BBB",color[0],color[1],color[2])

    return string

def lightpack(colors):
        string = pack("B", len(colors)/3)

        string += colors

        return string

def getmssscreen():
    with mss() as sct:
        sct_img = sct.grab(sct.monitors[1])
        img = Image.new("RGB", sct_img.size)
        # Image.frombytes("RGB", (geom.width, geom.height), str(sct_img.raw), "raw", "BGRX")
        # pixels = zip(sct_img.raw[2::4], sct_img.raw[1::4], sct_img.raw[0::4])
        # return pixels

def fromonescreen():
    colors = []

    raw = root.get_image(0, 0, geom.width,geom.height, X.ZPixmap, 0xffffffff)

    for y in xrange(1,steps[1]):
        colors.append(Image.frombytes("RGB", (10, (steps[1]-y)*H), raw.data, "raw", "BGRX").getpixel((0, 0)))

    for x in xrange(1,steps[0]):
        colors.append(Image.frombytes("RGB", (x*W, 10), raw.data, "raw", "BGRX").getpixel((0, 0)))

    for y in xrange(1,steps[1]):
        colors.append(Image.frombytes("RGB", (geom.width-10, y*H), raw.data, "raw", "BGRX").getpixel((0, 0)))

    return colors

def getcolorslight():
    colors = b""

    for y in xrange(1,steps[1]):
        colors += root.get_image(10, (steps[1]-y)*H, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]

    for x in xrange(1,steps[0]):
        colors += root.get_image(x*W, 10, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]

    for y in xrange(1,steps[1]):
        colors += root.get_image(geom.width-10, y*H, 1,1, X.ZPixmap, 0xffffffff).data[0:3][::-1]

    return colors


def getcolors():

    colors = []

    for y in xrange(1,steps[1]):
        raw = root.get_image(10, (steps[1]-y)*H, 1,1, X.ZPixmap, 0xffffffff)
        colors.append(Image.frombytes("RGB", (1, 1), raw.data, "raw", "BGRX").getpixel((0, 0)))

    for x in xrange(1,steps[0]):
        
        raw = root.get_image(x*W, 10, 1,1, X.ZPixmap, 0xffffffff)
        colors.append(Image.frombytes("RGB", (1, 1), raw.data, "raw", "BGRX").getpixel((0, 0)))

    for y in xrange(1,steps[1]):
        
        raw = root.get_image(geom.width-10, y*H, 1,1, X.ZPixmap, 0xffffffff)
        colors.append(Image.frombytes("RGB", (1, 1), raw.data, "raw", "BGRX").getpixel((0, 0)))

    return colors


# start = time.time()
# colors = getcolors()
# aftercolor = time.time()
packed = packcolors(getcolors())
# fromos = time.time()
# packedmore = fromonescreen()

# frommss = time.time()
# mmscolors = getmssscreen()
# collighttime = time.time()
collight = lightpack(getcolorslight())
# end = time.time()

# print("getcollight:" + str(end-collighttime))

# print("frommms:" + str(collighttime-frommss))

# print("fromonescreen:" + str(frommss-fromos))

# print("packcolors:" + str(fromos-aftercolor))

# print("getcolors:" + str(aftercolor-start))

# print("start prog to getcolors:" + str(start-startprog))

print(packed)
print(collight)

print([ord(c) for c in packed])
print([ord(c) for c in collight])