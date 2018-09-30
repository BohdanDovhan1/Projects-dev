#include<SoftwareSerial.h>

#define TxD 3
#define RxD 2
#define LED_PIN 11
 

SoftwareSerial bluetoothSerial(TxD, RxD);

char c;

void setup() {
  bluetoothSerial.begin(9600);
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
   pinMode(10, INPUT); 
  }

void loop() {
  delay(50);
  if(bluetoothSerial.available()){
    c = bluetoothSerial.read();
    Serial.print(c);
    
    if (digitalRead(10) == HIGH){  //When button pressed it sents wrong ACK
      bluetoothSerial.write("b");
    }
    if(c=='1'){
      digitalWrite(LED_PIN, HIGH);
      bluetoothSerial.write('1');
       delay(50);
       digitalWrite(LED_PIN, LOW);
    }

if(c=='2'){ //handshake
      digitalWrite(LED_PIN, HIGH);
      bluetoothSerial.write('2');
       delay(50);
       digitalWrite(LED_PIN, LOW);
}


    
    if(c=='0'){     
      digitalWrite(LED_PIN, LOW);
      bluetoothSerial.write("b");
    }
  }}
