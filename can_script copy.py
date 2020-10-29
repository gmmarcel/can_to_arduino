import can
from can.bus import BusState

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

        self.f_status        = FunctionItem("Status", send,)
        self.f_last_event    = FunctionItem("Read last Event", Screen().input, ["Enter the function: "])
        self.f_temperature   = FunctionItem("Temperature", Screen().input, ["Enter the function: "])
        self.f_reset         = FunctionItem("Reset", Screen().input, ["Enter the function: "])
        self.f_settings      = FunctionItem("Configurate CAN", config_interface)



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
                        print(msg)

            except KeyboardInterrupt:
                pass  # exit normally

    def send(self):
        pass
    def save_csv(self):
        pass
    def cleanup(self):
        pass
    def print(self):
        pass


def config_interface():
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

    can_bustype = input("Bustype:")                             or config.bustype
    can_channel = input("Channel 0 or 1: ")                     or config.channel
    can_bitrate = input("Bitrate of CAN: ")                     or config.bitrate
    can_appname = input("Only Vector Hardware needed Appname:") or config.app_name #"ivas_"+time.strftime("%Y_%m_%d-%H_%M_%S")
    filename    = input("Filename to save the data: ")          or config.filename

    print("")
    print("##############################")
    print("# Bustype : "+can_bustype)
    print("# Channel : "+str(can_channel))
    print("# Bitrate : "+str(can_bitrate))
    print("# App Name: "+str(can_appname))
    print("# Filename: "+filename+".csv")
    print("##############################")
    print("")
    overwrite = input("Save new configuration (y/n): ")

    if(overwrite == "y"):
        config.bustype  = can_bustype
        config.app_name = can_appname
        config.channel  = can_channel
        config.bitrate  = can_bitrate
        config.filename = filename
    else:
        print("Didn't save the new configuration")
    
    #return can_bustype, can_appname, can_channel, can_bitrate, filename

def test():
    print(can_bustype)

def receive():
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

def send():
    pass



def main_menu():
    # Create the root menu
    menu = ConsoleMenu(
        title="Heusel Innovations GmbH",
        subtitle="CAN Read and Send Data",
        prologue_text="info text"
    )

    f_status        = FunctionItem("Status", send,)
    f_last_event    = FunctionItem("Read last Event", Screen().input, ["Enter the function: "])
    f_temperature   = FunctionItem("Temperature", Screen().input, ["Enter the function: "])
    f_reset         = FunctionItem("Reset", Screen().input, ["Enter the function: "])
    f_settings      = FunctionItem("Configurate CAN", config_interface)



    # Create a menu item that calls a function
    #function_item = FunctionItem("Fun item", Screen().input, kwargs={"prompt": "Enter an input: "})

    # Add all the items to the root menu
    menu.append_item(f_status)
    menu.append_item(f_last_event)
    menu.append_item(f_temperature)
    menu.append_item(f_reset)
    menu.append_item(f_settings)

    # Show the menu
    #menu.start()
    #menu.join()
    menu.show(True)



if __name__ == "__main__":
    #exec(open('receive.py').read())
    #t1 = threading.Thread(target=receive)
    #t1.daemon = True
    #t1.start()
    can = Service()

    can.main_menu()
