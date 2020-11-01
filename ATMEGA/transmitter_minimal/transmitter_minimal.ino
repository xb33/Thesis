/**
 * Copyright (c) 2009 Andrew Rapp. All rights reserved.
 *
 * This file is part of XBee-Arduino.
 *
 * XBee-Arduino is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * XBee-Arduino is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with XBee-Arduino.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <XBee.h>
 /*
 This example is for Series 1 XBee
 Sends a TX16 or TX64 request with the value of analogRead(pin5) and checks the status response for success
 Note: In my testing it took about 15 seconds for the XBee to start reporting success, so I've added a startup delay
 */

XBee xbee = XBee();

const int ledPin = 13;
int txCount = 0;
int buttonState = 0 ;


// allocate two bytes for to hold a 10-bit analog reading
byte prueba[]={ 0x48 ,0x6F ,0x6C, 0x61 ,0x20 ,0x58 ,0x42 ,0x65 ,0x65};
// with Series 1 you can use either 16-bit or 64-bit addressing
// 16-bit addressing: Enter address of remote XBee, typically the coordinator
Tx16Request tx = Tx16Request(0x0000, prueba, sizeof(prueba));
// 64-bit addressing: This is the SH + SL address of remote XBee
//XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x4008b490);
// unless you have MY on the receiving radio set to FFFF, this will be received as a RX16 packet
//Tx64Request tx = Tx64Request(addr64, payload, sizeof(payload));
TxStatusResponse txStatus = TxStatusResponse();


void transmit(){
  xbee.send(tx);
  Serial.println("Packet Transmited!");
    // after sending a tx request, we expect a status response
    // wait up to 0.8 seconds for the status response
    if (xbee.readPacket(800)) {
        Serial.println("Packet Received!");
        // got a response!
        // should be a znet tx status              
        if (xbee.getResponse().getApiId() == TX_STATUS_RESPONSE) {
            Serial.println("ACK Received!");
            xbee.getResponse().getTxStatusResponse(txStatus);
            // get the delivery status, the fifth byte
            if (txStatus.getStatus() == SUCCESS) {
                Serial.println("Success");
            }
            else {
                // the remote XBee did not receive our packet. is it powered on?
                Serial.println("Error 01");
            }
        }
    }
    else if (xbee.getResponse().isError()) {
        //nss.print("Error reading packet.  Error code: ");  
        //nss.println(xbee.getResponse().getErrorCode());
        // or flash error led
        Serial.println("Error 02");
    }
    else {
        // local XBee did not provide a timely TX Status Response.  Radio is not configured properly or connected
        Serial.println("Error 03");
    }
  }

void setup() {
  pinMode(ledPin,INPUT);
  Serial.begin(38400);
  xbee.setSerial(Serial);
    
}

void loop() {
  buttonState = digitalRead(ledPin);
  if ((buttonState == HIGH) && (txCount == 0)){
    Serial.println("State High");
    transmit();
    txCount+=1; 
  }
  while (buttonState== LOW ){
    Serial.println("State Low");
    delayMicroseconds(10);
    buttonState = digitalRead(ledPin);
    txCount = 0 ;
  }



  }





  

 
  



