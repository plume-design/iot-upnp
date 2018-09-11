# -*- coding: utf-8 -*-
import asyncio

from .SSDP import SSDP
from .HTTP import HTTP

from random import randrange

class Annoncer:
    """
    Annoncer main class
    """

    def __init__(self, device):
        self.device = None
        self.loop = asyncio.get_event_loop()

        #SSDP entry
        self.ssdp = SSDP(self, device.bindAddr)
        self.http = HTTP(self, device.port, device.bindAddr, device.secured)
        self.device = device
        self.configId = randrange(32000)

    def initLoop(self, loop=None):
        """
        Initialise an asyncio loop to handle network packages
        """
        if loop != None:
            self.loop = loop

        self.http.initLoop(self.loop)
        self.ssdp.initLoop(self.loop)

    def notify(self):
        self.ssdp.notify()

    def bye(self):
        pass

    def dispose(self):
        """
        Clear loop
        """
        self.ssdp.dispose()
        self.http.dispose()

    def foreaver(self):
        """
        Run loop forever (test)
        """
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        self.dispose()
        self.loop.close()
