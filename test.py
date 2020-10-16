import socket

import sys
import os
import config
import threading
from consolemenu import *
from consolemenu.items import *

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
    host = 'test123'        # Symbolic name meaning all available interfaces
    port = 12345     # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    print(host , port)
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:

        try:
            data = conn.recv(1024)

            if not data: break

            print("Client Says: "+data)
            conn.sendall("Server Says:hi")

        except socket.error:
            print("Error Occured.")
            break

    conn.close()

def send():
    host = "test123"
    port = 12345                   # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))



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
    menu.start()
    menu.join()


if __name__ == "__main__":
    t1 = threading.Thread(target=receive)
    t1.start()
    main_menu()