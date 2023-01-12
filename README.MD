# 1 what is it

It is a simulated version of a screen ambilight client server combination.
The client can run on a esp32 microcontroller that steers a neopixel rgb led string.
Or can run on a simulated controller based on a pygame graphical screen to simulate a led string.
All based on python/micropython.
The server is based on twisted and will sample colors of the screen and send them to the client.
The protocol i, udp based.

# 1.2 why care

It is a nice way to get ambilight on a monitor, perhaps it could be faster since python is not the fastest language, but it works.

# 2 how to use it

Basics:
1 install pipenv https://pypi.org/project/pipenv/
2 in this directorys run : pipenv shell
3 pipenv install (to install all the packages)

# 2.1 client

for now only the simulated client (the real client is based on micropython on a esp32 but this should be easy enough)

when in the pipenv environment you can got to the simulator dir and run ./simulate_client.py
This will show you a pygame screen with the simulated led strip (they will be all black if you dont have a server running)
So lets get a server running

# 1.2 server

when in the pipenv virt environment activated by (pipenv shell): twistd -y server.py
Now the server is running (it will run imediatly in the background)
Check runnig or not with (ps -A |grep twistd)

# 3 parts of the software

root dir:
main.py (this is what needs to run on a esp32 microcontroller, not sure if it still works)
server.py (the twisted server part)
settings.yml (is this still used ?)

lib dir:
dnsquery.py (it is a dns server lib, used for a capture portal for a esp32 but is it used here ?)
filehelper.py (the beginning of a structured file writer reader for dicts, crude key value store)
mesg_type.py (a lib that will distribute network messages by packet type incoming and outgoing)
messages.py (a lib that will encode and decode network messages)
microDNSSrv (it ties in with dnsquery or is a replacement, i guess it is not used by this project)
websettings.py (it is a webserver lib, but i guess it is not used by this project as well)
ws28##.py (libs that are needed by the esp32 micropython, not for the simulator)

simulator dir:
simulator_client.py (the esp32 neopixel simulator)
tneopixel (the simulator replacement for ws28xx with pygame to show the neopixel led srip om screen)
