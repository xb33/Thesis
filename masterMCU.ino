// MASTER MCU TO CONTROL THE SLAVES THAT CONTAINS THE END DEVICE AND THE JAMMER W/ RELAY
#include <millisDelay.h>

const int JAMMER_PIN = 8;
const int END_PIN = 13;

unsigned long DELAY_TIME = 500; //  sec
unsigned long delayStart = 0; // the time the delay started

bool delayRunning = false; // true if still waiting for delay to finish
bool jammerOn = false; // keep track of the led state
bool devicesOn = false;

void setup() {
  pinMode(JAMMER_PIN, OUTPUT);
  pinMode(END_PIN, OUTPUT);
  
  digitalWrite(JAMMER_PIN, LOW);
  digitalWrite(END_PIN, LOW);

  delayStart = millis();
  delayRunning = true;
  
  jammerOn = false;
  devicesOn = false;
  Serial.begin(38400);
}

void loop() {
  if (delayRunning && ((millis() - delayStart) >= DELAY_TIME)){
    delayStart += DELAY_TIME;
    devicesOn = ! devicesOn;
    jammerOn = ! jammerOn;
    if (devicesOn){
      digitalWrite(devicesOn, HIGH);
      digitalWrite(jammerOn,HIGH);
    }
    else{
      digitalWrite(devicesOn,LOW);
      digitalWrite(jammerOn,LOW);
    }
    
    
    
  }


}
