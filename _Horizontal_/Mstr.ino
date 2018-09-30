#include<SoftwareSerial.h>

#define TxD 3
#define RxD 2
#define LED_PIN 7

 

SoftwareSerial bluetoothSerial(TxD, RxD);

int c;
int count = 0;


void setup() {
            
  delay(50);
  pinMode(9,OUTPUT); digitalWrite(9,HIGH); 
  bluetoothSerial.begin(9600);
  Serial.begin(9600);
  Serial.println("Scanning Received Signal Strength Indicator(RSSI) + Querying + Broadcasting Hello");
 
   pinMode(LED_PIN, OUTPUT);
   pinMode(10, OUTPUT);  
   pinMode(A1, OUTPUT); 

 label:     //  Handshake loop
  delay(500);          
   bluetoothSerial.write('2'); 
       digitalWrite(LED_PIN, HIGH);
       delay(100);
       digitalWrite(LED_PIN, LOW);
       if(bluetoothSerial.available())
       c = bluetoothSerial.read();
        Serial.print("Hello");
        if (c=='2'){     
       Serial.println(" ");
       Serial.println("Connected");}
        
       else goto label;
       
}


void loop() {

  delay(50);          
  bluetoothSerial.write('1'); // Sending packets
       digitalWrite(LED_PIN, HIGH);
       delay(50);
       digitalWrite(LED_PIN, LOW);


   if (Serial.available())
       digitalWrite(LED_PIN, HIGH);
       delay(50);
       digitalWrite(LED_PIN, LOW);
   bluetoothSerial.write(Serial.read());

   if(bluetoothSerial.available() == NULL){  // If no responce
       digitalWrite(10, HIGH);
       delay(50);
       digitalWrite(10, LOW);

      tone(A1, 200);
      delay(50);
      noTone(A1);
   Serial.print("NoACK");
    count = count + 1;
    if (count == 30){
    Serial.println(" ");
    Serial.println("No response");
    Serial.println("Disconnecting");
    digitalWrite(9,LOW);
     delay(50);
     count = 0;
     setup();
     }
    }


  if(bluetoothSerial.available()){
    c = bluetoothSerial.read();
    if(c=='1'){
    Serial.write(c);
    
    }
    if(c!= '1'){   // If wrong ACK
       digitalWrite(10, HIGH);
       delay(50);
       digitalWrite(10, LOW);
      tone(A1, 200);
      delay(50);
      noTone(A1);
    Serial.write("fail");
     count = count + 1;
     if (count == 10){
      delay(50);
    Serial.println(" ");
    Serial.println("Error rate is too high");
    Serial.println("Disconnecting");
    digitalWrite(9,LOW);
     delay(500);
     count = 0;
     setup();
     }
   
    }}}

  
