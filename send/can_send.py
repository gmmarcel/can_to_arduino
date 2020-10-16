'''
Created on 29.09.2020

@author: Marcel Gruber

This script recievs, send and stores data send by a connected Microcontroller. 
All parameters can be set by flags or in the attached config.py file.
If you choose to use flags, they are used instead of the configuration.
'''
import can
from can.bus import BusState

import os
import argparse, sys
from datetime import datetime
import time

def send_one(can_command):

    with can.interface.Bus(
        bustype='vector', app_name='CANalyzer', channel=1, bitrate=500000
    ) as bus:


        msg = can.Message(
            arbitration_id=0x10, data=[can_command, 25, 0, 1, 3, 1, 4, 1], is_extended_id=False
        )

        try:
            bus.send(msg)
            print("Message sent on"+bus.channel_info)
            print("Command: "+str(msg))
        except can.CanError:
            print("Message NOT sent")


print("Config CAN BUS")
print("##################")
can_command  = input("Command for Arduino: ")
print("###########################################")
send_one(int(can_command))