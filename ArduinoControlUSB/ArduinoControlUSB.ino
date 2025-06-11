#include <Ultrasonic.h>
#include <Servo.h>
#include "track.h"
Servo myservo;  // 建立一個 servo 物件，最多可建立 12個 servo
int pos = 180;  // 設定 Servo 位置的變數

float error = 0;
bool hasFloat = false;
bool running = false;

Ultrasonic ultrasonic(22, 23);
int distance;

void setup() {
  myservo.attach(24);
  myservo.write(90);
  Serial.begin(9600);
}

void loop() {
  while(Serial.available()){
    char s = Serial.read();
    else if(s=='s'){
      running = 1;
    }
    while (running) {
    distance = ultrasonic.read();
    if(s>='0'&&s<='9'){
      myservo.write(10*(s-'0'));
    }
    /*tracking(error);
    if (buf[0] == 'n') {
      error = 0;
      Rotate();
    }*/
    if(s == 'p'){
      running = 0;
    }
    else if(s == 'e'){
      hasFloat = 1;
    }
  }
}