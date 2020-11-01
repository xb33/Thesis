# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 12:50:13 2020

DEFINITE CODE TO READ THE NEW LOG FILES FROM PYTHON (USING THE TESTING_RX & TX)
FOR NOW ONLY INTERESTED TO READ THE ADDRESS, RSSI FIELD
@author: NalV
"""
## ABRO EL ARCHIVO EN MODO LECTURA
datos = open(r"C:\Users\NalV\Documents\Python\RxSide\maytest.log",'r')
data = datos.readlines()

comp = "OperatingMode.ESCAPED_API_MODE:"
sen = "SENT"
rec = "RECEIVED"
start = "7E"

count_sent = 0
count_recv = 0
count_64 = 0
timest = []
# USING THE FRAME WITH 64-BIT ADDRESS AND PAYLOAD "Hello XBEE"
for row in data:
    a = row.split()
    ##EACH INDEX IS A ELEMENT FOLLOWING ORDER TIME-PORT-REC-OPERATINGMODE-FRAME
    ## ONLY ANALIZE THE PKT RECEIVED WITH API MODE
    if len(a)>4:
        if a[4] == rec and a[6] == comp:
            timestmp = a[0]
            if a[10] == '80':
                count_64 +=1
                frame = a[7:len(a)]
                sfd = a[7]
                l = a[8:10]
                typ = a[10]
                addr = a[11:19]
                rss = a[19]
                opt = a[20]
                rfd = a[21:len(a)]

        
        
        
        
    
    

            

        

        
    
