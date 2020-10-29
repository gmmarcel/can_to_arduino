import can
from can.bus import BusState
from can import Bus, Logger

import sys
import os
import config
import threading
from consolemenu import *
from consolemenu.items import *

class Service():

    def __init__(self):
        t1 = threading.Thread(target=self.receive)
        t1.daemon = True
        t1.start()


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

    def main(self):
        pass
    def main_menu(self):
        # Create the root menu
        self.menu = ConsoleMenu(
            title="Heusel Innovations GmbH",
            subtitle="CAN Read and Send Data",
            prologue_text="info text"
        )

        self.f_status        = FunctionItem("Status", self.send,)
        self.f_last_event    = FunctionItem("Read last Event", Screen().input, ["Enter the function: "])
        self.f_temperature   = FunctionItem("Temperature", Screen().input, ["Enter the function: "])
        self.f_reset         = FunctionItem("Reset", Screen().input, ["Enter the function: "])
        self.f_settings      = FunctionItem("Configurate CAN", self.config_interface)



        # Create a menu item that calls a function
        #function_item = FunctionItem("Fun item", Screen().input, kwargs={"prompt": "Enter an input: "})

        # Add all the items to the root menu
        self.menu.append_item(self.f_status)
        self.menu.append_item(self.f_last_event)
        self.menu.append_item(self.f_temperature)
        self.menu.append_item(self.f_reset)
        self.menu.append_item(self.f_settings)

        # Show the menu
        #menu.start()
        #menu.join()
        self.menu.show(True)

    def split_data(self, msg):
        #Timestamp -> msg.timestamp
        #ID -> msg.arbitration_id
        #Extended ID -> msg.is_extended_id (TRUE/FALSE)
        #DLC -> msg.dlc
        #Channel -> msg.channel
        data_string = ''
        if msg.dlc > 0:
            data_string = ' '.join('{:02X}'.format(x) for x in msg.data)
        x = data_string.split(" ")
        x2 = x[0].split()
        print(x2)
        #pass
    
    def log_all(self, msg):
        #Log all incoming and outgoing data to a file
        logger = Logger('log_can4')
        logger(msg)

    def receive(self):
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
                        self.split_data(msg)
                        #self.log_all(msg)
                        #pass

            except KeyboardInterrupt:
                pass  # exit normally

    def send(self):
        pass
    
    def convert_ascii(self):
        pass
    def save_csv(self):
        pass
    def cleanup(self):
        pass
    def print(self):
        pass


if __name__ == "__main__":
    #exec(open('receive.py').read())
    #t1 = threading.Thread(target=receive)
    #t1.daemon = True
    #t1.start()
    #logger = Logger('log_can4')
    can = Service()

    can.main_menu()
