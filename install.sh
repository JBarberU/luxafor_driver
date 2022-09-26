#!/bin//bash

echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04d8", ATTR{idProduct}=="f372" MODE="0664", GROUP="plugdev"' > /etc/udev/rules.d/luxafor.rules
udevadm control --reload
udevadm trigger
