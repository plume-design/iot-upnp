#!/usr/local/bin/python3 -u

import os
import sys
import upnp

def main():
    device = upnp.Device()
    device.deviceType = 'urn:sadmin-fr:device:demo:1'
    device.friendlyName = 'Demo UPnP Device'
    device.manufacturer = 'Bontiv'
    device.manufacturerURL = 'https://github.com/bontiv/'
    device.Description = 'A simple device witch open the project URL on double-click'
    device.modemName = 'DEMO-UPnP'
    device.modelNumber = 'DEMO-1.0'
    device.presentationURL = 'https://bontiv.github.io/iot-upnp/'

    service = upnp.Service()
    device.addService(service)

    server = upnp.Annoncer(device)
    server.initLoop()
    server.notify()
    server.foreaver()
    server.dispose()

if __name__ == "__main__":
    sys.exit(main())
