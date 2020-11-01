# -*- coding: utf-8 -*-
#PROGRAMA PARA LEER LOS PAQUETES XBEE RECIBIDOS
#UTILIZANDO LA LIBRERIA OTORGADA POR DIGI-XBEE
#IMPORTANDO CLASE ESPECIFICA DE DISPOSITIVO 802.15.4

"""
Created on Wed Jan 29 12:12:39 2020

@author: NalV
"""
from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice

device=XBeeDevice("COM7",9600)
device.open()
sync = 5 #Seconds
mes = "Tu mama es weona y era"

remote_xbee = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20040761FF8"))
device.send_data(remote_xbee,mes)
device.set_sync_ops_timeout(sync)
remote_xbee.read_device_info()