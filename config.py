'''
configuration details for the can_data.py script,
general paramters for establishing the connection 
as well as mode specific parameters to select the
desired output and storage
'''

#Mode Selection 'logging' or 'interact'
channel = 1
bustype = "vector"
bitrate = 500000
app_name = "CANalyzer"

filename = "data_logger"

#Commands to Send
command = [1, 2, 3, 4, 5]

test = "test"