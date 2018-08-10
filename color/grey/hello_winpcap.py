#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install pypiwin32 winpcapy

from winpcapy import WinPcapDevices

# Return a list of all the devices detected on the machine
print((WinPcapDevices.list_devices()))

from winpcapy import WinPcapUtils

print((WinPcapUtils.capture_on_and_print("*Microsoft*")))
