from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import time

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM7"



# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

DATA_TO_SEND = "Hello XBee!"

PACKETS_TRANSMIT = 100

i = 0

device = XBeeDevice(PORT, BAUD_RATE)

device.open()

remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0x0013A20040761FF8") )

while( i <= PACKETS_TRANSMIT):
    ## INSERT THE ADDRESS OF THE COORDINATOR AS REMOTE XBEE
    device.send_data(remote_device , "Hello XBEE")
    i += 1

if device is not None and device.is_open():
    device.close()

        
