int in1=2;
int in2=3;
int en1=6;

void setup() {
  Serial.begin(9600);  // Set baud rate to match Python script
  pinMode(2,OUTPUT);
 pinMode(3,OUTPUT);
 pinMode(6,OUTPUT);  // Assuming LED is connected to pin 3
}

void loop() {
  digitalWrite(in1,HIGH);
  
  digitalWrite(in2, LOW);

  
  if (Serial.available() > 0) {

    
    byte incomingByte = Serial.read(); // Receive byte

    if (incomingByte == 'n'){
      analogWrite(6,0);
    }
    else if (incomingByte == '7') { // Compare byte to ASCII value of '1'
      // Turn on LED if human is detected
     analogWrite(6,255);}
    else if (incomingByte == '10') { // Compare byte to ASCII value of '1'
      // Turn on LED if human is detected
      analogWrite(6,200);}
    else if (incomingByte == 'h') { // Compare byte to ASCII value of '1'
      // Turn on LED if human is detected
      analogWrite(6,150);}

}}