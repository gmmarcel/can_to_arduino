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

if __name__ == "__main__":
    receive_all()