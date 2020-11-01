# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:42:37 2020


CODE TO ANALYZE THE LOG DATA IN THE TRANSMITTER SIDE USING PUTTY
@author: NalV
"""
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import math
from datetime import datetime
import time

i=0
c_success = 0
c_error1 = 0
c_error2 = 0
c_error3 = 0
c_pkt = 0
rec = []
y = []
x = []

## First the success and then the time stamp.
## 2n == events , 2n+1 == time stamps

time_suc = []

with open(r'C:\Users\NalV\Documents\Definitive_CE_DATA\April_13\Four\threetx_com7_0ms' , 'r') as archivo:
    data = archivo.readlines()
   
for linea in data:
    if len(linea)>2:       
        elem = linea.split(" ")
        fecha = elem[0]
        time = elem[2]
        dat = elem[3:5]
        ##
        if dat != "\n":
            for l in dat:
                if l == "Success\n":
                    c_success += 1
                    time_suc.append("Success")
                    time_suc.append(time.replace("]",""))
                if l == "01\n":
                    c_error1  += 1
                    time_suc.append("Error 01")
                    time_suc.append(time.replace("]",""))
                if l == "02\n":
                    c_error2  += 1
                    time_suc.append("Error 02")
                    time_suc.append(time.replace("]",""))
                if l == "03\n":
                    c_error3  += 1
                    time_suc.append("Error 03")
                    time_suc.append(time.replace("]",""))
                if l == "Received!\n":
                    rec.append("Received")
                    rec.append(time.replace("]",""))

        
print("El numero de mensajes Success es: ")        
print(c_success)
print("El numero de mensajes Error 01 es: ")        
print(c_error1)
print("El numero de mensajes Error 02 es: ")        
print(c_error2)
print("El numero de mensajes Error 03 es: ")        
print(c_error3)
        
while i < (len(time_suc)):
   if i==0 or i%2 ==0:
       y.append(time_suc[i])
   else:
       x.append(time_suc[i])
   i +=1
        
timest = []

for da in x:
    timestmp = datetime.strptime(da,'%H:%M:%S:%f')
    timest.append(timestmp)

datenums=md.date2num(timest)
values=y
plt.subplots_adjust(bottom=0.2)
plt.xticks( rotation=25 )
ax=plt.gca()
xfmt = md.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(datenums,values)
plt.show()
        
        
        
#plt.xlabel("Time H:M:S:ms")
#plt.ylabel("Events")   
#plt.title("Occurrence of each event") 





# while i<len(time_suc):
#     ## THE PAIRS CORRESPOND TO THE EVENTS
#     init = time_suc[1]
#     init_int = init.replace("[","")
#     end = time_suc[len(time_suc)-1]
#     end_int = end.replace("]","")
#     if i==0 or i%2==0:    
#         if time_suc[i] == 'Success':
#             y = 1
#         if time_suc[i] == 'Error 01':
#             y = 2
#         if time_suc[i] == 'Error 02':
#             y = 3
#         if time_suc[i] == 'Error 03':
#             y = 4
#         fig = plt.figure()
#         ax = fig.add_axes([0.1, 0.5, 0.8, 0.8]) 
#         ax.scatter(time_suc[i+1], time_suc[i])
#         ax.set_xticks([0,math.ceil(len(time_suc)/2),len(time_suc)-1])
#         #plt.plot(time_suc[i+1] , y , ls = ':' , lw = 0.3 , c = 'black' , marker= '+' , ms = 10 , mfc='blue')
#         #plt.xticks
#         #plt.yticks(np.arange(4),['Success','Error 01','Error 02','Error 03'])     
#         #plt.xticks([0,math.ceil(len(time_suc)/2), len(time_suc)-1],[init, time_suc[math.ceil(len(time_suc)/2)], end_int])
#     i+=1
# plt.show()
    
    
