import can
from can.interface import Bus
from can.message import Message
from can.bus import BusState
from can import Bus, Logger

import sys
from os import system, name 
import config
import copy 
from queue import Queue 
import threading
from datetime import datetime


class Service():

    def __init__(self):
        pass

    def data_cache(self):
        pass

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
                        #self.log_all(msg)
                        #print("check_data")
                        #self.check_data(msg, out_q)
                        out_q.put(msg)
                        #print(msg)
                        #pass

            except KeyboardInterrupt:
                pass  # exit normally

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
            pass
            #self.convert_hex(msg, hex_data, out_q)

    def send(self, i):
        self.command = config.command[i]
        #print("test_send_data")
        with Bus(
            bustype='vector', app_name='CANalyzer', channel=1, bitrate=500000
        ) as bus:

            msg = Message(
                arbitration_id=0x10, dlc=1, data=[self.command], is_extended_id=False
                )

            try:
                bus.send(msg)
                #print("Message sent on"+bus.channel_info)
                #print("Command: "+str(msg))
                return msg
            except can.CanError:
                print("Message NOT sent")

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

            return "Saved the new configuration"
        else:
            return "Didn't save the new configuration"

    # define our clear function 
    def clear(self): 
        self.info = ""
        self.msg_send = ""
        self.msg_receive = ""
        # for windows 
        print(name)
        if name == 'nt': 
            _ = system('cls') 
  
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 
        
    def print_menu(self, heartbeat, info, msg_send, msg_receive):       ## Your menu design here
        self.title  	= "Heusel Innovations GmbH"
        self.subtitle   = "CAN Data Send and Receive"
        menutitle   = [
            "1. Stauts",
            "2. Temperature",
            "3. Other Sensors",
            "4. Read last Event",
            "5. Reset",
            "6. Configurate CAN",
            "7. Exit"]
        

        print(80 * "-")
        print("""
            """+self.title+""""
            """+self.subtitle+"""
            """)
        print(80 * "-")
        print("\nHEARTBEAT:")
        print(heartbeat)
        print("\nINFO:")
        print(info)
        print("\nMessage Sent:")
        print(msg_send)
        print("\nMessage Received:")
        print(msg_receive)
        print(80 * "-")
        #print(30 * "-" , "MENU" , 31 * "-")
        print("\nMENU")
        print("""      """+menutitle[0]+
            """\n      """+menutitle[1]+
            """\n      """+menutitle[2]+
            """\n      """+menutitle[3]+
            """\n      """+menutitle[4]+
            """\n      """+menutitle[5]+
            """\n      """+menutitle[6])
        print(80 * "-")

    def menu(self, in_q):
        self.info        = ""
        self.msg_send    = ""
        self.msg_receive = ""

        loop=True     
        
        while loop:          ## While loop which will keep going until loop = False
            heartbeat = in_q.get()
            self.print_menu(heartbeat, self.info, self.msg_send, self.msg_receive)    ## Displays menu
            choice = int(input("Enter your choice [1-5]: "))
            
            if choice==1: #Status
                self.clear()
                self.info           = "Status"
                self.msg_send       = self.send(0)
                self.msg_receive    = in_q.get()
                
            elif choice==2: #Temperature
                self.clear()
                self.info           = "Temperature"
                self.msg_send    = self.send(1)

                i = 0
                data_list = []

                with Bus(
                    bustype='vector', app_name='CANalyzer', channel=1, bitrate=500000
                ) as bus:
                # set to read-only, only supported on some interfaces
                #bus.state = BusState.PASSIVE

                    try:
                        while i != 2 :
                            msg = bus.recv(1)
                            if msg.dlc > 0:
                                data_string = ' '.join('{:02X}'.format(x) for x in msg.data)
                                hex_data = data_string.split(" ")
                            if (hex_data[0].lower() == "14" or hex_data[0].lower() == "15"):
                                self.msg_receive = str(msg)+"\n"
                                i = i+1

                    except KeyboardInterrupt:
                        pass  # exit normally
                self.msg_receive = data_list

            elif choice==3: #Other Sensors
                self.clear()
                self.info           = "Other Signals"
                self.msg_send    = self.send(2)
                self.msg_receive = in_q.get()

            elif choice==4: #Read last Event
                self.clear()
                self.info           = "Read last Event"
                self.msg_send    = self.send(3)
                self.msg_receive = in_q.get()
            
            elif choice==5: #Reset
                self.clear()
                self.info           = "Reset"
                self.msg_send    = self.send(4)
                self.msg_receive = in_q.get()

            elif choice==6: #Configurate CAN
                self.clear()
                self.info = self.config_interface()

            elif choice==7:
                print("Menu 5 has been selected")
                ## You can add your code or functions here
                loop=False # This will make the while loop to end as not value of loop is set to False
                quit()

            else:
                # Any integer inputs other than values 1-5 we print an error message
                input("Wrong option selection. Enter any key to try again..")

if __name__ == "__main__":
    can = Service()
    can.clear()
    # Create the shared queue and launch both threads 
    q = Queue()    
    t1 = threading.Thread(target = can.menu, args =(q, ))
    t2 = threading.Thread(target = can.receive, args =(q,), daemon=True) 
    t1.start()
    t2.start()
