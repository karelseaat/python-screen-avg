
import socket
import gc
import time
from filehelper import makefileifneed
from websettings import websettings
from machine import Pin
import network
import math

def brightness(cols, change):
    if change <= 0:
        change = (change*-1)+0000.1

    if change >= 1:
        change = 1/change

    # there should be a per color difference in the change since humans eyes and brains, it shall be later.

    return int(cols[0]*change), int(cols[1]*change), int(cols[2]*change)

def saturation(cols, change):
    p = colorsqrt(cols)

    R=p+((cols[0])-p)*change
    G=p+((cols[1])-p)*change
    B=p+((cols[2])-p)*change

    return (R,G,B)

def normalisation(cols):
    mins = min(cols[0], cols[1], cols[2])
    if mins < 0:
        cols = (cols[0]+(-1*mins), cols[1]+(-1*mins), cols[2]+(-1*mins))

    sums = (cols[0]) + (cols[1]) + (cols[2]) + 1
    r = cols[0]/sums*255
    g = cols[1]/sums*255
    b = cols[2]/sums*255
    
    return(r,g,b)

def colorsqrt(cols):
    return math.sqrt(
        (cols[0]*cols[0]) +
        (cols[1]*cols[1]) +
        (cols[2]*cols[2])
    )

def allthemultycasts(sta_if):
    return ".".join(sta_if.ifconfig()[0].split('.')[0:3])+'.255'

def dimColors(colors, dim):
    color1 = 0 if (colors[0] - dim[0]) < 0 else colors[0] -  dim[0]
    color2 = 0 if (colors[1] - dim[1]) < 0 else colors[1] -  dim[1]
    color3 = 0 if (colors[2] - dim[2]) < 0 else colors[2] -  dim[2]
    return color1, color2, color3

def connection(network_name, network_password):
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



def accespointmode():
    from microDNSSrv import MicroDNSSrv
    websets.setTemplate('set_ap.html')
    websets.setregexp(['networkname','password'])
    websets.addTempVars({'ssid':'networkname','pass':'password'})

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='temp-ambi', authmode=1)
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '192.168.4.1'))
 
    domainsList = {"*":"192.168.4.1"}
    mdns = MicroDNSSrv()
    mdns.SetDomainsList(domainsList)
    mdns.Start()


    while True:
        mdns._serverProcess()
        
        websets.WEBQnA()

        # time.sleep_ms(100)

def clientmode(existing_config):
    from message import Message
    from neopixel import NeoPixel
    

    
    np = NeoPixel(Pin(2), 32)
    mes = Message()
    station = connection(existing_config['networkname'],existing_config['password'])

    multip = allthemultycasts(station)

    so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    so.setblocking(False)
    so.sendto('register',(multip,5544))


    timeout = 0

    while True:
        
        pixels = []
        length = 1

        try:
            timeout = 0
            
            data,addr = so.recvfrom(1024)
            mes.add(data)

            pixels = mes.unpack_color_ar()

        except Exception as e:
            so.sendto('register',(multip,5544))
            time.sleep_ms(10)
            
            if timeout < 8000:
                timeout += 1

            for pix in range(np.n):
                np[pix] = dimColors(np[pix], (int(timeout/32),int(timeout/32),int(timeout/32)))

            np.write()


        incrementer = length / np.n 
        acount = 0
        while acount < np.n and pixels:
            # print(normalisation(saturation(pixels[int(acount*incrementer)],1.3)))
            np[acount] = brightness(normalisation(saturation(pixels[int(acount*incrementer)],1.3)),0.2)

            acount += 1

        np.write()
        mes.discard()


def captive_portal(websets):
    import usocket as socket
    
    existing_config = websets.test_config() 

    if not existing_config:
        accespointmode()
    else:
        clientmode(existing_config)
            
websets = websettings()

clear = Pin(0)
if not clear.value():
    print("clearing settings !")
    websets.clear_settings()

captive_portal(websets)