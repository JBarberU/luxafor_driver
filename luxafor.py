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

    def fade_to(self, led, r, g, b, time):
        self._write([0x02, led, r, g, b, time, 0])

    def set_color(self, led, r, g, b):
        self._write([0x01, led, r, g, b, 0, 0])

    def strobe(self, led, r, g, b, speed, repeat):
        self._write([0x03, led, r, g, b, speed, 0, repeat])

    def wave(self, wave_type, r, g, b, repeat, speed):
        self._write([0x4, wave_type, r, g, b, 0, repeat, speed])

    def built_in(self, pattern, repeat):
        self._write([0x6, pattern, repeat, 0, 0, 0, 0, 0])

    def _write(self, command):
        self.dev.write(1, command)



def rgb_from_hex(hex_color):
    hex_color = hex_color.strip('#').strip()
    return(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )




def call_func(func, device, led, r, g, b, speed, repeat, type_):
    func(device, led, r, g, b, speed, repeat, type_)


def main():
    commands = {
        'set-color': lambda d, led, r, g, b, speed, repeat, type_: d.set_color(led, r, g, b),
        'fade':      lambda d, led, r, g, b, speed, repeat, type_: d.fade_to(led, r, g, b, speed),
        'strobe':    lambda d, led, r, g, b, speed, repeat, type_: d.strobe(led, r, g, b, speed, repeat),
        'wave':      lambda d, led, r, g, b, speed, repeat, type_: d.wave(type_, r, g, b, repeat, speed),
        'built-in':  lambda d, led, r, g, b, speed, repeat, type_: d.built_in(type_, repeat),
        'off':       lambda d, led, r, g, b, speed, repeat, type_: d.fade_to(0xff, 0, 0, 0, 10),
    }

    parser = argparse.ArgumentParser(description='Set Luxafor state')
    parser.add_argument('--command', choices=commands.keys(), help='Command to run')
    parser.add_argument('--color', '-c', help='Color in hex value, #ff00ff for instance')
    parser.add_argument('--leds', '-l', type=int, choices=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0xFF, 0x41, 0x42], help='')
    parser.add_argument('--speed', '-s', type=int, help='Speed (fade-in/wave/strobe)')
    parser.add_argument('--repeat', '-r', type=int, help='Repeats (0-255 -> 0 = infinite)')
    parser.add_argument('--type', '-t', type=int, help='Type (1-5 for wave or 0-8 for built-ins)')
    args = parser.parse_args()

    d = Device()
    r, g, b = rgb_from_hex(args.color) if args.color else (0,0,0)
    call_func(commands[args.command], d, args.leds, r, g, b, args.speed, args.repeat, args.type)


if __name__ == '__main__':
    main()
