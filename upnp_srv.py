#!/usr/bin/env python3

import argparse
import configparser
import logging
import os
import sys
import upnp

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__file__)

class Device:
    def __init__(self, conf):
        self.conf = os.path.abspath(conf)
        self.device = upnp.Device()
        self.config()

    def config(self):
        conf = configparser.ConfigParser()
        logger.debug("conf file: {}".format(self.conf))
        conf.read_file(open(self.conf))
        sections = (conf.sections())
        if 'DeviceConf' not in sections:
            logger.error("No [deviceConf] section in conf file %s" % self.conf)
            return 1
        section = 'DeviceConf'
        self.device.deviceType = conf[section]['deviceType'].strip()
        logger.debug("deviceType: {}".format(self.device.deviceType))

        self.device.friendlyName = conf[section]['friendlyName'].strip()
        logger.debug("friendlyName: {}".format(self.device.friendlyName))

        self.device.manufacturer = conf[section]['manufacturer'].strip()
        logger.debug("manufacturer: {}".format(self.device.manufacturer))

        if 'manufacturerURL' in conf[section]:
            self.device.manufacturerURL = conf[section]['manufacturerURL'].strip()
            logger.debug("manufacturerURL: {}".format(self.device.manufacturerURL))

        if 'modelDescription' in conf[section]:
            self.device.modelDescription = conf[section]['modelDescription'].strip()
            logger.debug("modelDescription: {}".format(self.device.modelDescription))

        self.device.modelName = conf[section]['modelName'].strip()
        logger.debug("modelName: {}".format(self.device.modelName))

        if 'modelNumber' in conf[section]:
            self.device.modelNumber = conf[section]['modelNumber'].strip()
            logger.debug("modelNumber: {}".format(self.device.modelNumber))

        self.device.secured = conf.getboolean(section, 'secured')
        logger.debug("secured: {}".format(self.device.secured))

        if 'bindAddr' in conf[section]:
            self.device.bindAddr = conf[section]['bindAddr'].strip()
            logger.debug("bindAddr: {}".format(self.device.bindAddr))

        self.device.port = conf.getint(section, 'port')
        logger.debug("port: {}".format(self.device.port))

def main():
    logger.setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", dest="conf", type=str,
                        help="UPnP configuration",
                        default='device.conf')
    parser.add_argument("--log-level", dest="loglevel",
                        choices=['INFO', 'DEBUG'],
                        default='INFO')
    args = parser.parse_args()

    # Set log level
    if args.loglevel == 'INFO':
        loglvl = logging.INFO
    else:
        loglvl = logging.DEBUG
    logging.basicConfig(level=loglvl, format=log_format)

    device = Device(args.conf)
    service = upnp.Service()
    device.device.addService(service)

    server = upnp.Annoncer(device.device)
    server.initLoop()
    server.notify()
    server.foreaver()
    server.dispose()

if __name__ == "__main__":
    sys.exit(main())
