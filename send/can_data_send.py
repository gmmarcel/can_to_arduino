#!/usr/bin/env python
'''
Created on 29.09.2020

@author: Marcel Gruber

This script recievs, send and stores data send by a connected Microcontroller. 
All parameters can be set by flags or in the attached config.py file.
If you choose to use flags, they are used instead of the configuration.
'''
import can
from can.bus import BusState

import config
import os
import argparse, sys
from datetime import datetime
import time



def receive_all():
    #Receives all messages and prints them to the console until Ctrl+C is pressed.

    with can.interface.Bus(
        bustype='vector', app_name='CANalyzer', channel=1, bitrate=500000
    ) as bus:
        # set to read-only, only supported on some interfaces
        #bus.state = BusState.PASSIVE

        try:
            while True:
                msg = bus.recv(1)
                if msg is not None:
                    print(msg)

        except KeyboardInterrupt:
            pass  # exit normally

def convert_message():
    #Convert all messages
    pass

def send_one(can_command):
    #Sends a single message.

    # this uses the default configuration (for example from the config file)
    # see https://python-can.readthedocs.io/en/stable/configuration.html
    with can.interface.Bus(
        bustype='vector', app_name='CANalyzer', channel=1, bitrate=500000
    ) as bus:

        # Using specific buses works similar:
        # bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
        # bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)
        # bus = can.interface.Bus(bustype='ixxat', channel=0, bitrate=250000)
        # bus = can.interface.Bus(bustype='vector', app_name='CANalyzer', channel=1, bitrate=500000)

        msg = can.Message(
            arbitration_id=0x10, data=[can_command, 25, 0, 1, 3, 1, 4, 1], is_extended_id=False
        )

        try:
            bus.send(msg)
            print("Message sent on"+bus.channel_info)
            print("Command: "+str(msg))
        except can.CanError:
            print("Message NOT sent")

def send_status():
        # Identifier 10
        # DLC 1
        # Data 7 (Command) 0
        pass
def config_interface(can_bustype, appname, can_channel, can_bitrate, filename, interface, can_command):
    #Dialog to start script
    print("Config CAN BUS")
    print("##################")
    #can_bustype = input("Bustype:")                             or can_bustype
    #appname     = input("Only Vector Hardware needed Appname:") or appname #"ivas_"+time.strftime("%Y_%m_%d-%H_%M_%S")
    #can_channel = input("Channel 0 or 1: ")                     or can_channel
    #can_bitrate = input("Bitrate of CAN: ")                     or can_bitrate
    #filename    = input("Filename to save the data: ")          or filename
    can_command  = input("Command for Arduino: ")                or can_command
    #print("###########################################")
    #print("#INFO######################################")
    #print("Interface Bus: Bustype="+can_bustype+", AppName= "+appname+", Channel= "+can_channel+", Bitrate= "+can_bitrate)
    #print("Filename  :"+filename+".txt")
    print("###########################################")
    send_one(int(can_command)
    #return can_bustype, appname, can_channel, can_bitrate, filename, interface


def logging(can_bustype, appname, can_channel, can_bitrate, filename, interface):
    pass
    
def interact(can_bustype, appname, can_channel, can_bitrate, filename, interface):
    #Dialog to start script
    if interface:
        pass
        #can_bustype, appname, can_channel, can_bitrate, filename, interface = config_interface(can_bustype, appname, can_channel, can_bitrate, filename, interface)
    with can.interface.Bus(
        bustype=can_bitrate,
        app_name=appname,
        channel=can_channel,
        bitrate=can_bitrate
    ) as bus:
        pass


if __name__ == "__main__":
    #send_one()
    #receive_all()

    parser = argparse.ArgumentParser()
    parser.add_argument("--command", help="Send command to Arduino", type=int, default=0)
    parser.add_argument("--mode", help="Decide between Interact or logging", default="interact")
    parser.add_argument("--bustype", help="Type of Bus", default='vector')
    parser.add_argument("--app_name", help="Needed only with Vector Hardware", default="CANalyzer")
    parser.add_argument("--channel", help="Channel 0 or 1", type=int, default=1)
    parser.add_argument("--bitrate", help="Baudrate of CAN", type=int, default=500000)
    parser.add_argument("--display", action='store_true', required=False)

    parser.add_argument("--filename", help="Filename to store the data")
    parser.add_argument("--interface", action="store_true", help="enables user-friendly interface for parameter input")

    args = parser.parse_args()

    mode = args.mode if args.mode else config.mode

    if mode == 'interact':
        can_bustype = args.bustype if args.bustype else config.bustype
        appname     = args.app_name if args.app_name else config.app_name
        can_channel = args.channel if args.channel else config.channel
        can_bitrate = args.bitrate if args.bitrate else config.bitrate
        filename    = args.filename if args.filename else config.filename
        interface   = args.interface if args.interface else config.interface
        can_command = args.command if args.command else config.command

        config_interface(can_bustype, appname, can_channel, can_bitrate, filename, interface, can_command)

    if mode == 'logging':
        can_bustype = args.bustype if args.bustype else config.bustype
        appname     = args.app_name if args.app_name else config.app_name
        can_channel = args.channel if args.channel else config.channel
        can_bitrate = args.bitrate if args.bitrate else config.bitrate
        filename    = args.filename if args.filename else config.filename
        interface   = args.interface if args.interface else config.interface

        interact(can_bustype, appname, can_channel, can_bitrate, filename, interface)
    
    if mode == 'send':
        can_command = args.command if args.command else config.command

        send_one(can_command)

"""
    except OSError as e:  # FileExistsError:
        logging.error("Could not create database (file exists?)")
        logging.debug(e)
    except KeyboardInterrupt:
        logging.info("Got keyboard interrupt")
        #logging.info("stored data in: " + file + ', ' + csv_path + ', ' + csv_path.replace('.csv', '_high_acc.csv') )
        """