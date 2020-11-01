# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 15:52:47 2020
CODE FOR THE TRANSMITTER SIDE.
@author: NalV
"""
import random
import string
from digi.xbee.devices import XBeeDevice
import logging




def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
# Instantiate an XBee device object.
device = XBeeDevice("COM1", 9600)
device.open()
# create logger with 'spam_application'
logger = logging.getLogger('collision_experiments')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('ex.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


# Instantiate a remote XBee device object.
remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20040XXXXXX"))
# Send data using the remote object.
ans=True
while ans:
    print("""
    1. Use a fixed message
    2. Use a random message
    """ )
    ans=raw_input("What kind of transmission do you want? : ")
    if ans == "1":
        message = raw_input ("Enter the fixed message that you want to transmit: ")
        
    elif ans == "2":
        message = randomString()
    l_message.append(message)    
    device.send_data(remote_device, message)



