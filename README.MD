 # Project Overview

This repository contains the source code for a custom network configuration and lighting control system implemented in Python for LoRaWAN devices, specifically a LoPy board. The project is divided into several modules that handle various aspects of the application such as web interface, MicroDNSSrv for DNS services, and WS2812 LED control among others.

## Key Components

- **Web Interface**: Implemented using Flask, this component provides a user-friendly HTML form to set up the network access point (SSID and password) and customize the color settings of an integrated RGB LED strip.
- **MicroDNSSrv**: A MicroPython implementation of the Dnsmasq DNS server that allows for easy hostname configuration and dynamic IP address management on the LoRaWAN network.
- **LED Control**: Utilizing the WS2812 library, this component manages an RGB LED strip connected to a LoPy board, enabling custom lighting configurations based on user input from the web interface.

## Features

- **Network Configuration**: Users can set up their own access point network easily using the provided web interface.
- **LED Customization**: Users can adjust the brightness and saturation of the integrated RGB LED strip through the web interface, providing a simple way to customize the appearance of the device.

## Requirements

To run this project, you'll need the following:

- A LoPy board with a WS2812 RGB LED strip connected to it
- microPython installed on your LoRaWAN device
- Twisted, Xlib, PyYAML, Pygame, Pylint packages installed (see `Pipfile` for installation instructions)

## Usage

To use the project, follow these steps:

1. Flash MicroPython onto your LoRaWAN device using the appropriate tool (e.g., Espressif's Thonny or Microsoft's Visual Micro).
2. Install the required packages listed in `Pipfile`.
3. Upload the entire contents of this repository to your LoRaWAN device using a suitable file transfer method (e.g., serial console or FTP).
4. Connect the RGB LED strip to the appropriate pins on the LoPy board as described in the WS2812 library documentation.
5. Once everything is set up, power on your device and access the web interface by connecting to the newly created network (SSID and password provided through the web interface). Configure the network settings, and customize the LED color settings as desired.