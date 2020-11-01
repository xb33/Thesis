from __future__ import division
from collections import Counter
import re
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
rssi=[]
addresses=[]
ide=[]
## CONTADORES 
contador_coma=0
contador_espacio=0
contador_envio=0
contador_recibo=0
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
## DATOS COMPARACION TRAMA LEGITIMA CONSIDERANDO TRAMA FIJA EN BITS
## INGRESAR EN HEX , LUEGO LA FUNCION LOS TRANSFORMARA
txData = ('0000000FFFFFFFF0000686F6C61')
txAddress = ('0001')
txOption = ('00')
txType = ('01')
rxType =('81')
txLen = ('0012')
#txLsb = (' ')
#txMsb = (' ')
txCrc = ('4E')
txSfd = ('7E')
txId = ('01')
bin_data , bin_address , bin_option , bin_type , bin_len , bin_crc , bin_id , bin_sfd = ([] for i in range(8))
## DATOS COMPARACION TRAMAS NO LEGITIMAS, PARA EL ESCENARIO TODO IGUAL SOLO EL 
# ADDRESS SERA DIFERENTE
interfer1_address = ('')
interfer2_address = ('')
## AÑADIR VARIABLE PARA ALMACENAR LOS DATOS EN EL CASO ALEATORIO LAS TRAMAS
# PARA ELLO GENERAR TRAMAS CON EL MISMO LENGTH PERO CON RANDOM DATA
#
#
#
#
#
## ABRO EL ARCHIVO EN MODO LECTURA
datos = open("G:\UdeChile\Investigacion\python_cCodes\data.log",'r')
data = datos.readlines()
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
#def cuentoBer(y,z):
#    cuento_ber=0
#    indice=0
#    if(len(y)==len(z)):
#        while(indice < len(y)):
#            for digitos1 in y[indice]:
#                for digitos2 in z[indice]:
#                    if digitos1!=digitos2:
#                        cuento_ber+=1
#            indice+=1  
#    else:
#        print("El largo de las listas no coincide (ERROR)")   
#    return cuento_ber 
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
    #SI ES ACK , RECV, SENT U OTRO
    #TRANSMISSION STATUS / ACK
    if (frame[6:8])=='8B':
        contador_ack+=1
        #SUCCESS
        if (frame[16:18])=='00':
            contador_success+=1
        else:
            contador_fail+=1
    # ES UN PAQUETE TX REQUEST    
    else:
        #SI ES RECV ENTONCES CONSIDERAR QUE LOS CAMPOS[8:14] DIFIEREN DEL SENT
        if trama_total[3]=='RECV':
            contador_recibo+=1
            #FRAME TYPE TIENE QUE SER 81
            bin_type = aBits(rxType)        
            bin_rec_type = aBits(frame[6:8])
            contador_ber_type = contador_ber_type + cuentoBer(bin_rec_type,bin_type) 
            #ADDRESS
            #dec_add = int(conv[10:recorro_byte-1])        
            addresses.append(frame[8:12])
            bin_rec_address = aBits(frame[10:14])
            #RSSI
            rss = int(frame[8:10])
            rssi.append(rss)        
        #ENTONCES ES SEND
        else: 
            contador_envio+=1
            addresses.append(frame[10:14])
            #FRAME TYPE TIENE QUE SER 01
            bin_type = aBits(rxType)        
            bin_rec_type = aBits(frame[6:8])
            contador_ber_type = contador_ber_type + cuentoBer(bin_rec_type,bin_type) 
            #FRAME ID NO ESTIMO NECESARIO ANALIZARLO, PUESTO QUE ES UN CONTADOR
            #POR AHORA SOLO LO ALMACENARE 
            #bin_id = aBits(txId)
            #bin_rec_id = aBits(frame[8:10])
            #contador_ber_id= contador_ber_id + cuentoBer(bin_rec_id,bin_id)   
            ide.append(frame[8:10])
        #LOS SIGUIENTES FIELDS SON COMUN PARA AMBOS PAQUETES   
        bin_sfd = aBits(txSfd)    
        bin_rec_sfd = aBits(frame[0:2])
        contador_ber_sfd = contador_ber_sfd + cuentoBer(bin_rec_sfd,bin_sfd)        
        #LENGTH
        bin_len = aBits(txLen)
        bin_rec_len = aBits(frame[2:6])
        contador_ber_len = contador_ber_len + cuentoBer(bin_rec_len,bin_len)                        
        #contador_ber_address = contador_ber_address + cuentoBer(bin_rec_address,bin_address)            
        #OPTIONS
        bin_option = aBits(txOption)
        bin_rec_option = aBits(frame[14:16])
        contador_ber_option = contador_ber_option + cuentoBer(bin_rec_option,bin_option)             
        #PAYLOAD AND CRC 
        bin_data = aBits(txData)
        bin_rec_data = aBits(frame[16:len_tot-1])
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
##IMPRIMO LOS DIFERENTES VALORES ANALIZADOS
print("El numero de ACK contados en total es de ")
print(contador_ack)
print("El numero de ACK success es de ")
print(contador_success)
print("El numero de ACK erroneos es de ")
print(contador_fail)
print("El numero de paquetes recibidos es de ", total_rec )
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






 
       
            
            
   
    
            
            
        
        
    
       
    
    
    
    