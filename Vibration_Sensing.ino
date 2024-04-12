#include<Servo.h>

Servo servo1;

int motor = 8;
int vs =7;

void setup(){
  servo1.attach(8);
  pinMode(motor, OUTPUT);
  pinMode(vs, INPUT); 
  servo1.write(0);
  Serial.begin(9600); 

}
void loop(){
  long measurement =vibration();
  delay(50);
  Serial.println(measurement);
  if (measurement > 50){
    servo1.write(90);
    delay(5000);
  }
  else{
    servo1.write(0);
  }
}

long vibration(){
  long measurement=pulseIn (vs, HIGH);
  return measurement;
}