import can
from can.interface import Bus
from can.message import Message
from can.bus import BusState
from can import Bus, Logger

import sys
import os
import config
import copy 
from queue import Queue 
import threading
from datetime import datetime
from consolemenu import *
from consolemenu.items import *

class Service():

    def __init__(self):
        #print("started")
        #r = threading.Thread(target=self.receive)
        #r.daemon = True
        #r.start()
        pass

    def config_interface(self):
        #Dialog to start script
        print("Configurate CAN BUS")
        print("")
        print("##############################")
        print("# Bustype : "+config.bustype)
        print("# Channel : "+str(config.channel))
        print("# Bitrate : "+str(config.bitrate))
        print("# App Name: "+config.app_name)
        print("# Filename: "+config.filename)
        print("##############################")
        print("")

        self.can_bustype = input("Bustype:")                             or config.bustype
        self.can_channel = input("Channel 0 or 1: ")                     or config.channel
        self.can_bitrate = input("Bitrate of CAN: ")                     or config.bitrate
        self.can_appname = input("Only Vector Hardware needed Appname:") or config.app_name #"ivas_"+time.strftime("%Y_%m_%d-%H_%M_%S")
        self.filename    = input("Filename to save the data: ")          or config.filename

        print("")
        print("##############################")
        print("# Bustype : "+self.can_bustype)
        print("# Channel : "+str(self.can_channel))
        print("# Bitrate : "+str(self.can_bitrate))
        print("# App Name: "+str(self.can_appname))
        print("# Filename: "+self.filename+".csv")
        print("##############################")
        print("")
        self.overwrite = input("Save new configuration (y/n): ")

        if(self.overwrite == "y"):
            config.bustype  = self.can_bustype
            config.app_name = self.can_appname
            config.channel  = self.can_channel
            config.bitrate  = self.can_bitrate
            config.filename = self.filename
        else:
            print("Didn't save the new configuration")
        
        #return can_bustype, can_appname, can_channel, can_bitrate, filename

    def last_event(self):
        pass
    def send(self, i):
        self.main_menu(False)
        self.command = config.command[i]
        print("test_send_data")
        with Bus(
            bustype='vector', app_name='CANalyzer', channel=1, bitrate=500000
        ) as bus:

            msg = Message(
                arbitration_id=0x10, dlc=1, data=[self.command], is_extended_id=False
                )

            try:
                bus.send(msg)
                print("Message sent on"+bus.channel_info)
                print("Command: "+str(msg))
            except can.CanError:
                print("Message NOT sent")

    def status(self, i, in_q):
        print("Send Command")
        self.send(i)
        data = in_q.get()
        print(data)


    def main_menu(self, in_q):
        # Create the root menu
        #out_q = out_q
        self.menu = ConsoleMenu(
            title="Heusel Innovations GmbH",
            subtitle="CAN Read and Send Data",
            prologue_text="info text"
        )

        self.f_status        = FunctionItem("Status", self.status, args=[0, in_q])
        self.f_last_event    = FunctionItem("Temperature", self.send, args=[1])
        self.f_temperature   = FunctionItem("Other Sensors", self.send, args=[2])
        self.f_sensor        = FunctionItem("Read last Event", self.send, args=[3])
        self.f_reset         = FunctionItem("Reset", self.send, args=[4])
        self.f_settings      = FunctionItem("Configurate CAN", self.config_interface)



        # Create a menu item that calls a function
        #function_item = FunctionItem("Fun item", Screen().input, kwargs={"prompt": "Enter an input: "})

        # Add all the items to the root menu
        self.menu.append_item(self.f_status)
        self.menu.append_item(self.f_last_event)
        self.menu.append_item(self.f_temperature)
        self.menu.append_item(self.f_sensor)
        self.menu.append_item(self.f_reset)
        self.menu.append_item(self.f_settings)

        # Show the menu
        #self.menu.start()
        #self.menu.join()
        #self.menu.show(True)

    def check_data(self, msg, out_q):
        #print("check_data")
        data_string = ''
        if msg.dlc > 0:
            data_string = ' '.join('{:02X}'.format(x) for x in msg.data)
        hex_data = data_string.split(" ")

        if(hex_data[0].lower() == "0a"):
            pass
        else:
            #print("-------")
            self.convert_hex(msg, hex_data, out_q)

    def convert_hex(self, msg, data, out_q):
        #Timestamp -> msg.timestamp
        #ID -> msg.arbitration_id
        #Extended ID -> msg.is_extended_id (TRUE/FALSE)
        #DLC -> msg.dlc
        #Channel -> msg.channel
        #data_formatted = []
        #print("----------")
        print(msg)
        out_q.put(copy.deepcopy(msg))
        data_dec = []
        for i in data:
            conv = int(i,16)
            data_dec.append(conv)
        print(data_dec)
        #self.status_menu(data_dec)


        
        #print(data_string)
        #x2 = hex_data[0].split()
        #x3 = int(x2[0],16)
        #if (x3 == 30):
        #    for i in x:
        #        conv = int(i,16)
        #        data_formatted.append(conv)

            #print(data_string)

        #pass
    
    def log_all(self, msg):
        #Log all incoming and outgoing data to a file
        msg = msg
        log_file = open("log_can.txt","a")#append mode
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

        log_file.write(dt_string+" --- "+str(msg)+"\n")
        log_file.close()
        #print("closed file"+dt_string)

    def status_msg(self):
        print("Status")

    def receive(self, out_q):
        #Receives all messages and prints them to the console until Ctrl+C is pressed.
        #log_file = open("log_can.txt","a")#append mode
        with Bus(
            bustype='vector', app_name='CANalyzer', channel=1, bitrate=500000
        ) as bus:
            # set to read-only, only supported on some interfaces
            #bus.state = BusState.PASSIVE

            try:
                while True:
                    msg = bus.recv(1)
                    if msg is not None:
                        #print("schleife")
                        self.log_all(msg)
                        #print("check_data")
                        self.check_data(msg, out_q)
                        #print(msg)
                        #pass

            except KeyboardInterrupt:
                pass  # exit normally

    def convert_ascii(self):
        pass
    def save_csv(self):
        pass
    def cleanup(self):
        pass
    def print(self):
        pass
    def main(self):
        pass


if __name__ == "__main__":
    #exec(open('receive.py').read())
    #t1 = threading.Thread(target=receive)
    #t1.daemon = True
    #t1.start()
    #logger = Logger('log_can4')
    can = Service()

    # Create the shared queue and launch both threads 
    q = Queue() 
    t1 = threading.Thread(target = can.receive, args =(q, )) 
    t2 = threading.Thread(target = can.main_menu, args =(q, )) 
    t1.start() 
    t2.start()

    #can.main()
    #can.main_menu(True)
