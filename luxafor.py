#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time
import usb.core

class Commands:

    set_color = 0x01
    fade_to = 0x02

class Device:

    def __init__(self):
        self.dev = usb.core.find(idVendor=0x04d8, idProduct=0xf372)

        if self.dev is None:
            print('Not connected')
            return

        try:
            self.dev.detach_kernel_driver(0)
        except usb.core.USBError:
            pass

        try:
            self.dev.set_configuration()
        except usb.core.USBError as e:
            print("Unable to connect to USB device, have you run install.sh?")
            raise e

    def set_color(self, color):
        self._write_command(Commands.set_color, color, [0,0,0])

    def fade_to(self, color, speed):
        self._write_command(Commands.fade_to, color, [speed, 0, 0])

    def _write_command(self, command, color, arguments):
        self.target = 0x0
        if len(arguments) != 3:
            arguments = [0,0,0]

        # self.dev.write(command, [self.target, color] + arguments)
        args = [self.target, color] + arguments
        self.dev.write(command, args)


def main():
    color_codes = {
        'blue': 0x42,
        'cyan': 0x43,
        'green': 0x47,
        'magenta': 0x4d,
        'red': 0x52,
        'white': 0x57,
        'yellow': 0x59,

        'off': 0x4f,
    }

    commands = {
        'set_color': Device.set_color,
        'fade_in': Device.fade_to
    }

    parser = argparse.ArgumentParser(description='Change Luxafor colour')
    parser.add_argument('color', choices=color_codes.keys(), help='color to change to')
    args = parser.parse_args()


    d = Device()

    color = color_codes[args.color]
    d.set_color(color)


if __name__ == '__main__':
    main()
