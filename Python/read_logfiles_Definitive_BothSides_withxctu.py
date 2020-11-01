# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:43:03 2020
CODE TO READ AND PLOT AT THE SAME TIME THE DATA IN THE RECEIVER SIDE
AND ALSO IN EACH TRANSMITTER SIDE. WE NEED TO SPECIFY THE NAME OF THE FILES
IN ORDER TO DECODE THE DATA
@author: NalV
"""
from __future__ import division
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import re
from datetime import datetime
import matplotlib.dates as md
import time


# -*- coding: utf-8 -*-
# PROGRAMA PARA LEER LAS TRAMAS ENVIADAS Y RECIBIDAS EN EL ARCHIVO LOG
"""
Created on Mon Feb 17 13:58:17 2020
READ THE FRAMES 
@author: NalV
"""
##RECORRER
indice=0
digitos =0
##POSICIONES
com=[]
esp=[]
start_data=[]
#ALMACENAR
rssi_addr1 = []
rssi_addr2 = []
addresses=[]
timest = []
time_suc_t1 = []
time_suc_t2 = []
rec1 = []
rec2 = []

timerx1 = []
timerx2 = []

datex1 = []
datex2 = []

timest1 = []
timest2 = []
y1 = []
y2 = []
x1 = []
x2 = []
y = []
y_2 = []
## CONTADORES 
contador_coma=0
contador_espacio=0
contador_envio_16=0
contador_envio_64=0
contador_recibo_16=0
contador_recibo_64=0
contador_success =0
contador_fail =0
contador_ack=0
contador_ber_sfd = 0
contador_ber_payload=0
contador_ber_option=0
contador_ber_len=0
contador_ber_id=0
contador_ber_type=0
contador_ber_address = 0
contador_ber_crc = 0
bits_leidos = 0
sum_hex = 0
valid_packet=0
invalid_packet=0
c_success_t1 = 0
c_error1_t1 = 0
c_error2_t1 = 0
c_error3_t1 = 0
c_success_t2 = 0
c_error1_t2 = 0
c_error2_t2 = 0
c_error3_t2 = 0

## DATOS COMPARACION TRAMA LEGITIMA CONSIDERANDO TRAMA FIJA EN BITS
## INGRESAR EN HEX , LUEGO LA FUNCION LOS TRANSFORMARA
txData = ('48 6F 6C 61 20 58 42 65 65')
txData = txData.replace(" ","")
txAddress = ('0000')
txOption = ('00')
txLen = ('0014')
verif = ('FF')
#txLsb = (' ')
#txMsb = (' ')
txCrc = ('A3')
txSfd = ('7E')
#USADO PARA CONTRASTAR EL PKT UART CON EL RX
txId = ('01')
bin_data , bin_address , bin_option , bin_type , bin_len , bin_crc , bin_id , bin_sfd = ([] for i in range(8))
## DATOS COMPARACION TRAMAS NO LEGITIMAS, PARA EL ESCENARIO TODO IGUAL SOLO EL 
# ADDRESS SERA DIFERENTE
address_1 = '0013A2004091DCFE'
address_2 = '0013A20040761F53'
## AÑADIR VARIABLE PARA ALMACENAR LOS DATOS EN EL CASO ALEATORIO LAS TRAMAS
# PARA ELLO GENERAR TRAMAS CON EL MISMO LENGTH PERO CON RANDOM DATA

## ABRO CADA ARCHIVO EN MODO LECTURA
datosCoordinador = open(r'C:\Users\NalV\Documents\Definitive_CE_DATA\May_06\c0_1610_tatb0.log','r')
datosTransmisor1 = open(r'C:\Users\NalV\Documents\Definitive_CE_DATA\Data_BE3\29_2tx_60cm_BE3\com7_2tx_60cm_BE3' , 'r')
datosTransmisor2 = open(r'C:\Users\NalV\Documents\Definitive_CE_DATA\Data_BE3\29_2tx_60cm_BE3\com15_2tx_60cm_BE3' , 'r')


data = datosCoordinador.readlines()
dataTransmisor1 = datosTransmisor1.readlines()
dataTransmisor2 = datosTransmisor2.readlines()


## FUNCION PARA TRANSFORMAR LOS DATOS LEIDOS EN BINARIOS
def aBits(x):
    escala=16
    numero_bits=8
    lista_resultado=[]
    recorrido=0
    resultado=0
    while(recorrido<len(x)):
        resultado=bin(int(x[recorrido],escala))[2:].zfill(numero_bits)
        lista_resultado.append(resultado)
        recorrido+=1
    return lista_resultado
##FUNCION PARA CONTAR LOS ERRORES BER "Y" STRING A COMPARAR CON "Z"
def cuentoBer(x,y):
    cuento_ber = 0
    cuento_correcto = 0
    byte = 0
    #RECORRO TODAS LOS ELEMENTOS EN LA LISTA
    while(byte < len(x)):
        if(x[byte] != y[byte]):
            bit=0
            s = x[byte]
            t = y[byte]
            while(bit < len(s)):
                if s[bit] != t[bit]:
                    cuento_ber += 1
                else:
                    cuento_correcto +=1
                bit +=1
        byte+=1
    return cuento_ber
##PROGRAMA PRINCIPAL PARA LEER LOS DATOS CONTENIDOS EN EL ARCHIVO LOG
##TEMPLATE DE LOS DATOS  
#METODOLOGIA CONSISTE EN TRANSFORMAR LOS DATOS A COMPARAR A HEX
#Y LUEGO TOMAR EL CAMPO DE LA TRAMA CORRESPONDIENTE A LO QUE DESEAMOS COMPARAR
#PARA LUEGO INVOCAR LA FUNCION QUE CONTARA EL NUMERO DE ERRORES ENCONTRADOS
while(indice < len(data)-2):
    offset=2
    #GENERO UNA LISTA, SEPARO LA TRAMA A TRABAJAR POR ESPACIOS Y COMAS    
    trama_total = re.split('[\s,]{1}',data[indice+offset])
    ## [0] Fecha ; [1] Tiempo Rx ; [2] ID ; [3] Recv O Sent ; [4] Trama    
    frame = trama_total[4]
    bits_leidos = bits_leidos + len(frame) * 8
    len_tot = len(frame)
    #PRIMERO TENEMOS QUE SABER QUE TIPO DE PAQUETE VAMOS A ANALIZAR
    #SI ES ACK , RECV, SENT U OTRO, PARA ELLO ANALIZAR EL FRAME TYPE
    #ADEMAS TENEMOS LA INFORMACION DEL LOGGER DONDE NOS DICE SI LO RECIBIO O LO ENVIO
    #TRANSMISSION STATUS / ACK == 89
    ## TX REQUEST 64 == 00 ; TX REQUEST 16 == 01
    ## RX REQUEST 64 == 80 ; RX REQUEST 16 == 81
    if (frame[6:8])=='89':
        contador_ack+=1
        #SUCCESS
        if (frame[10:12])=='00':
            contador_success+=1
        else:
            contador_fail+=1
    # ES UN PAQUETE TX REQUEST 64    
    if (frame[6:8])=='00' and trama_total[3]=='SENT':
        txType = '00'
        contador_envio_64 +=1
        ##PARA CUANDO GENEREMOS EL ENVIO ALEATORIO DE PAQUETES, EN ESTAS LINEAS
        #EXTRAEREMOS CADA FIELD DE LA TRAMA PARA LUEGO CONTRASTARLA CON LOS RECV
    
    # ES UN PAQUETE TX REQUEST 16    
    if (frame[6:8])=='01' and trama_total[3]=='SENT': 
        txType = '01'
        contador_envio_16 +=1    
        
    # ES UN PAQUETE RX REQUEST 64    
    if (frame[6:8])=='80' and trama_total[3]=='RECV':
        contador_recibo_64+=1  
        rxType = '80' 
        #LOS SIGUIENTES FIELDS SON COMUN PARA AMBOS PAQUETES DE 64 BITS
        bin_sfd = aBits(txSfd)    
        bin_rec_sfd = aBits(frame[0:2])
        contador_ber_sfd = contador_ber_sfd + cuentoBer(bin_rec_sfd,bin_sfd)        
        #LENGTH
        bin_len = aBits(txLen)
        bin_rec_len = aBits(frame[2:6])
        contador_ber_len = contador_ber_len + cuentoBer(bin_rec_len,bin_len)                        
        #contador_ber_address = contador_ber_address + cuentoBer(bin_rec_address,bin_address)  
        #ADDRESS FIELD
        rec_address = frame[8:24]
        ##ALMACENAR VALORES PARA CADA TRANSMISOR
        if (rec_address == address_1 ):
            rss = frame[24:26]
            rssi_addr1.append(rss)
            timerx1.append(trama_total[1])
        if (rec_address == address_2):
            rss = frame[24:26]
            rssi_addr2.append(rss)
            timerx2.append(trama_total[1])
        addresses.append(rec_address)
        #bin_rec_address = aBits(frame[10:26])          
        ##RSSI
        rss = frame[24:26]       
        #OPTIONS
        bin_option = aBits(txOption)
        bin_rec_option = aBits(frame[26:28])
        contador_ber_option = contador_ber_option + cuentoBer(bin_rec_option,bin_option)             
        #PAYLOAD AND CRC 
        bin_data = aBits(txData)
        bin_rec_data = aBits(frame[28:len_tot-3])
#        contador_ber_payload = contador_ber_payload + cuentoBer(bin_rec_data,bin_data)
        #CRC CALCULATION ; ALL BYTES INCLUDING THE CRC AND EXCLUDING DE SFD AND LENGTH BYTES
        all_bytes = frame[6:len_tot-2]
        i=0
        sum_tot = 0
        sum_hex = 0        
        while i < len(all_bytes)-1:
            #PYTHON TRANSFORMA AUTOMATICAMENTE EL VALOR EN DECIMAL
            val_hex = all_bytes[i] + all_bytes[i+1]
            val2_hex = all_bytes[i+2] + all_bytes[i+3]
            sum_hex = int(val_hex,16) + int(val2_hex,16)
            sum_tot = sum_tot + sum_hex
            i += 4
        sum_total = hex(sum_tot)
        if sum_total[len(sum_total)-3:len(sum_total)-1] == 'FF':
            #CRC CORRECTO
            valid_packet+=1
        else:
            invalid_packet+=1
        #bin_crc = aBits(txCrc)    
        #bin_rec_crc = aBits(frame[len_tot-3:len_tot-1])
        #contador_ber_crc = contador_ber_crc + cuentoBer(bin_rec_crc,bin_crc)
    # ES UN PAQUETE RX REQUEST 16    
    if (frame[6:8])=='81' and trama_total[3]=='RECV':
        contador_recibo_16+=1
        rxType = '81'
        #LOS SIGUIENTES FIELDS SON COMUN PARA AMBOS PAQUETES DE 16 BITS
        bin_sfd = aBits(txSfd)    
        bin_rec_sfd = aBits(frame[0:2])
        contador_ber_sfd = contador_ber_sfd + cuentoBer(bin_rec_sfd,bin_sfd)        
        #LENGTH
        bin_len = aBits(txLen)
        bin_rec_len = aBits(frame[2:6])
        contador_ber_len = contador_ber_len + cuentoBer(bin_rec_len,bin_len)                        
        #contador_ber_address = contador_ber_address + cuentoBer(bin_rec_address,bin_address)            
        #ADDRESS FIELD
        rec_address = frame[8:12]
        addresses.append(rec_address)        
        #RSSI FIELD        
        rss = frame[12:14]     
        #OPTIONS
        bin_option = aBits(txOption)
        bin_rec_option = aBits(frame[14:16])
        contador_ber_option = contador_ber_option + cuentoBer(bin_rec_option,bin_option)             
        #PAYLOAD AND CRC 
        bin_data = aBits(txData)
        bin_rec_data = aBits(frame[16:len_tot-3])
        contador_ber_payload = contador_ber_payload + cuentoBer(bin_rec_data,bin_data)
        #CRC        
        bin_crc = aBits(txCrc)    
        bin_rec_crc = aBits(frame[len_tot-3:len_tot-1])
        contador_ber_crc = contador_ber_crc + cuentoBer(bin_rec_crc,bin_crc)
        #VACIO LAS LISTAS PARA ANALIZAR LA NUEVA TRAMA
        bin_rec_data , bin_rec_address , bin_rec_option , bin_rec_type , bin_rec_len , bin_rec_crc , bin_rec_id , bin_rec_sfd = ([] for i in range(8))
    #FRAME TYPE  
    indice+=1      
##CALCULO EL NUMERO DE TRAMAS RECIBIDAS DE CADA EMISOR
cuenta = Counter(addresses)
total_rec = sum(cuenta.values())

## ANALIZO LOS DATOS PARA LOS TRANSMISORES

for li in dataTransmisor1:
    if len(li)>2:       
        elem = li.split(" ")
        fecha = elem[0]
        time = elem[2]
        dat = elem[3:5]
        ##
        if dat != "\n":
            for l in dat:
                if l == "Success\n":
                    c_success_t1 += 1
                    time_suc_t1.append("Success")
                    time_suc_t1.append(time.replace("]",""))
                if l == "01\n":
                    c_error1_t1  += 1
                    time_suc_t1.append("Error 01")
                    time_suc_t1.append(time.replace("]",""))
                if l == "02\n":
                    c_error2_t1  += 1
                    time_suc_t1.append("Error 02")
                    time_suc_t1.append(time.replace("]",""))
                if l == "03\n":
                    c_error3_t1  += 1
                    time_suc_t1.append("Error 03")
                    time_suc_t1.append(time.replace("]",""))
                if l == "Received!\n":
                    rec1.append("Received")
                    rec1.append(time.replace("]",""))

    
for lin in dataTransmisor2:
    if len(lin)>2:       
        elem = lin.split(" ")
        fecha = elem[0]
        time = elem[2]
        dat = elem[3:5]
        ##
        if dat != "\n":
            for l in dat:
                if l == "Success\n":
                    c_success_t2 += 1
                    time_suc_t2.append("Success")
                    time_suc_t2.append(time.replace("]",""))
                if l == "01\n":
                    c_error1_t2  += 1
                    time_suc_t2.append("Error 01")
                    time_suc_t2.append(time.replace("]",""))
                if l == "02\n":
                    c_error2_t2  += 1
                    time_suc_t2.append("Error 02")
                    time_suc_t2.append(time.replace("]",""))
                if l == "03\n":
                    c_error3_t2  += 1
                    time_suc_t2.append("Error 03")
                    time_suc_t2.append(time.replace("]",""))
                if l == "Received!\n":
                    rec1.append("Received")
                    rec1.append(time.replace("]",""))



##IMPRIMO LOS DIFERENTES VALORES ANALIZADOS
print("El numero de ACK contados en total es de ")
print(contador_ack)
print("El numero de ACK success es de ")
print(contador_success)
print("El numero de ACK erroneos es de ")
print(contador_fail)
print("El numero de paquetes de 16-bits enviados es de " )
print(contador_envio_16)
print("El numero de paquetes de 64-bits enviados es de " )
print(contador_envio_64)
print("El numero de paquetes recibidos de 16-bits es de " )
print(contador_recibo_16)
print("El numero de paquetes recibidos de 64-bits es de " )
print(contador_recibo_64)
print("El numero de paquetes recibidos de cada address es de ")
print(cuenta)
print("Total de bits leidos")
print(bits_leidos)
print("El numero de errores en campo SFD es de : ")
print(contador_ber_sfd)
print("El numero de errores en campo Payload es de : ")
print(contador_ber_payload )
print("El numero de errores en campo Option es de : ")
print(contador_ber_option )
print("El numero de errores en campo Length es de : ")
print(contador_ber_len )
print("El numero de errores en campo ID  es de : ")
print(contador_ber_id)
print("El numero de errores en campo Frame Type es de : ")
print(contador_ber_type)
print("El numero de errores en campo Address es de : ")
print(contador_ber_address)
print("El numero de errores en campo CRC  es de : ")
print(contador_ber_crc)
print("El numero de mensajes Success es: ")        
print(c_success_t1, c_success_t2 )
print("El numero de mensajes Error 01 es: ")        
print(c_error1_t1 , c_error1_t2 )
print("El numero de mensajes Error 02 es: ")        
print(c_error2_t1 , c_error2_t2 )
print("El numero de mensajes Error 03 es: ")        
print(c_error3_t1 , c_error3_t2)

##PLOTEAR PARA CADA TRANSMISOR EN PARTE RECEPTORA
if len(rssi_addr1) > 0 :
    rssi_addr1 = [int(a,16) for a in rssi_addr1]
    dbm_addr1 = np.negative(rssi_addr1)
    vari_addr1 = np.var(dbm_addr1)
    desv1 = np.std(dbm_addr1)
    av1 = -1 * (sum(rssi_addr1)/len(rssi_addr1))

if len(rssi_addr2) > 0 :
    rssi_addr2 = [int(a,16) for a in rssi_addr2]
    dbm_addr2 = np.negative(rssi_addr2)
    vari_addr2 = np.var(dbm_addr2)
    desv2 = np.std(dbm_addr2)
    av2 = -1 * (sum(rssi_addr2)/len(rssi_addr2))

print("El valor promedio de RSSI para cada transmisor es de :  " ,av1 , av2)
print("Varianza RSSI:", vari_addr1, vari_addr2)
print("Desviacion Estandar RSSI", desv1 , desv2)

if ( len(rssi_addr1) and len(rssi_addr2) )>0:
    ##GRAFICANDO LOS VALORES DE RSSI. SE ASUME QUE CADA VALOR ALMACENADO CORRESPONDE
    #AL PAQUETE RECIBIDO CADA 2(S) SIN IMPORTAR EL SENDER NODE
    #CONVERTIR VALORES A -DBM
    fig0 = plt.figure()
    plt.axhline(y=av1,color='r',linestyle='-', lw = 2)
    plt.axhline(y=av2,color='m',linestyle='-', lw = 2)
    plt.xlabel("Packets Received ID")
    plt.ylabel("RSSI in dBm (decimal) ")
    plt.title("RSSI values through experiment ")
    x22 = np.arange(0,len(dbm_addr2))
    x11 = np.arange(0,len(dbm_addr1))
    plt.plot(x11 , dbm_addr1 , ls = ':' , lw = 0.1 , c = 'black' , marker= '+' , ms = 10 , mec='blue' , label = 'E1')
    plt.plot(x22 , dbm_addr2 , ls = ':' , lw = 0.1 , c = 'yellow' , marker= '+' , ms = 10 , mec='green', label ='E2')
    plt.legend(loc="center right")
    plt.show()

## PLOTEAR PARA VER EL ORDEN DE LOS EVENTOS Y SU OCURRENCIA
## TRANSFORMO LOS DATOS A LOS EJES X E Y PARA PLOTEAR 
while i < (len(time_suc_t1)):
           if i==0 or i%2 ==0:
               y1.append(time_suc_t1[i])
           else:
               x1.append(time_suc_t1[i])
       
           i +=1
f=0
while f < (len(time_suc_t2)):  
           if f==0 or f%2 ==0:
               y2.append(time_suc_t2[f])
           else:
               x2.append(time_suc_t2[f])
           f +=1

for da in x1 :
    timestmp = datetime.strptime(da,'%H:%M:%S:%f')
    timest1.append(timestmp)
    
for da in x2 :
    timestmp = datetime.strptime(da,'%H:%M:%S:%f')
    timest2.append(timestmp)

for da in timerx1 :
    timestmp = datetime.strptime(da,'%H:%M:%S.%f')
    datex1.append(timestmp)
    
    
for da in timerx2 :
    timestmp = datetime.strptime(da,'%H:%M:%S.%f')
    datex2.append(timestmp)    



datenums1 = md.date2num(timest1)
datenums2 = md.date2num(timest2)

datenums3 = md.date2num(datex1)
datenums4 = md.date2num(datex2)


values1 = y1
values2 = y2

## PLOTTING TX SIDE EVENTS VS TIMESTAMP
fig1 = plt.figure()
plt.subplots_adjust(bottom= 0.2)
plt.xticks( rotation = 25 )
ax = plt.gca()
xfmt = md.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
fig1.suptitle('Events reported in time for E1')
plt.plot(datenums1,values1)

fig2 = plt.figure()
plt.subplots_adjust(bottom= 0.2)
plt.xticks( rotation = 25 )
ax = plt.gca()
xfmt = md.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
fig2.suptitle('Events reported in time for E2')
plt.plot(datenums2,values2)

##PLOTTING RX SIDE RSSI VS TIMESTAMP RECORDED

fig3 = plt.figure()
plt.subplots_adjust(bottom= 0.2)
plt.xticks( rotation = 25 )
ax = plt.gca()
xfmt = md.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
fig3.suptitle('RSSI values referred to the timestamp for E1 (RxSide)')
plt.plot(datenums3,dbm_addr1)

fig4 = plt.figure()
plt.subplots_adjust(bottom= 0.2)
plt.xticks( rotation = 25 )
ax = plt.gca()
xfmt = md.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
fig4.suptitle('RSSI values referred to the timestamp for E2 (RxSide)')
plt.plot(datenums4,dbm_addr2)

plt.show()
 
       
            
            
   
    
            
            
        
        
    
       
    
    
    
    

