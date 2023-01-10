
import socket
import gc
import time
# from filehelper import makefileifneed
from lib.websettings import websettings
from machine import Pin
import network
import math
from microDNSSrv import MicroDNSSrv

PIXELS = None
LIGHTCONFIG = None

def brightness(cols, change):
    """the right way to change brightness acoring to fumulas and shite"""
    if change <= 0:
        change = (change*-1)+0000.1

    if change >= 1:
        change = 1/change

    # there should be a per color difference in the change
    # since humans eyes and brains, it shall be later.

    return int(cols[0]*change), int(cols[1]*change), int(cols[2]*change)

def saturation(cols, change):
    """change the saturation of the color,
    dont know how or where, perhaps later this will change"""
    compund = colorsqrt(cols)

    red=compund+((cols[0])-compund)*change
    green=compund+((cols[1])-compund)*change
    blue=compund+((cols[2])-compund)*change

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
        (cols[0]*cols[0]) +
        (cols[1]*cols[1]) +
        (cols[2]*cols[2])
    )

def allthemultycasts(sta_if):
    """get the multycast address from the interface
    (current network parameters)"""
    return ".".join(sta_if.ifconfig()[0].split('.')[0:3])+'.255'

def dim_colors(colors, dim):
    """ this will take the color and substact points of every rgb color
        channel and return that color
        this will be done do slowly dimm the color
    """
    color1 = 0 if (colors[0] - dim[0]) < 0 else colors[0] -  dim[0]
    color2 = 0 if (colors[1] - dim[1]) < 0 else colors[1] -  dim[1]
    color3 = 0 if (colors[2] - dim[2]) < 0 else colors[2] -  dim[2]
    return color1, color2, color3

def connection(network_name, network_password):
    """Attempt to connect to accesspoint when you connect return the connection
    . . . connection is station"""
    attempts = 0
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print("Connecting to network...")
        station.active(True)
        station.connect(network_name, network_password)
        while not station.isconnected():
            print(f"Attempts: {attempts}")
            attempts += 1
            time.sleep(5)
            if attempts > 3:
                return None
    print('Network Config:', station.ifconfig())
    return station



def accespointmode():
    """will change to accespoint mode so you can go to its page and set it up,
    (to connect to the home accespoint so it is on the network)"""

    websets.setTemplate('set_ap.html')
    websets.setregexp(['networkname','password'])
    websets.addTempVars({'ssid':'networkname','pass':'password'})

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='temp-ambi', authmode=1)
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '192.168.4.1'))

    domains_list = {"*":"192.168.4.1"}
    mdns = MicroDNSSrv()
    mdns.SetDomainsList(domains_list)
    mdns.Start()


    while True:
        mdns.serverProcess()

        websets.WEBQnA()

        # time.sleep_ms(100)

def handleincomingpixels(mesg, _addr):
    PIXELS = mesg

def handleincomingconfig(mesg, _addr):
    LIGHTCONFIG = mesg


def clientmode(existing_config):
    # from message import Message
    from neopixel import NeoPixel
    from mesg_type import MesgType


    global PIXELS, LIGHTCONFIG

    msgtype = MesgType()

    msgtype.addfunctonum(handleincomingpixels, 0)
    msgtype.addfunctonum(handleincomingconfig, 1)

    np = NeoPixel(Pin(2), 90)
    # mes = Message()
    station = connection(
        existing_config['networkname'],
        existing_config['password']
    )

    multip = allthemultycasts(station)

    main_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    main_socket.setblocking(False)
    main_socket.sendto(msgtype.type_send_register(),(multip,5544))

    timeout = 0

    while True:

        PIXELS = []
        length = 1

        try:
            timeout = 0
            data,addr = main_socket.recvfrom(1024)
            msgtype.decodetype(data, addr)

        except Exception as error:
            print(error)

            main_socket.sendto(msgtype.type_send_register(),(multip,5544))
            time.sleep(0.01)

            if timeout < 8000:
                timeout += 1

            for pix in range(np.n):
                np[pix] = dim_colors(
                    np[pix],
                    (int(timeout/32),int(timeout/32),int(timeout/32))
                )

            np.write()

        incrementer = length / np.n
        acount = 0
        while acount < np.n and PIXELS:
            np[acount] = brightness(
                normalisation(
                    saturation(
                        PIXELS[int(acount*incrementer)],
                        LIGHTCONFIG['saturation']
                    )
                ),
                LIGHTCONFIG['brightness']
            )
            acount += 1
        np.write()


def captive_portal(websets):
    import usocket as socket

    existing_config = websets.test_config()

    if not existing_config:
        accespointmode()
    else:
        clientmode(existing_config)

websets = websettings()

# clear = Pin(0)
# if not clear.value():
#     print("clearing settings !")
#     # websets.clear_settings()

captive_portal(websets)
