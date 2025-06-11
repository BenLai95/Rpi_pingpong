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
  Serial2.begin(9600);
  myservo.write(170);
}

void loop() {
  while (Serial2.available()) {
    char s = Serial2.read();
    if (s == 's') {
      running = 1;
      Serial.println("Start Running");
    } else if (s == 'n') {
      error = 0;
      Rotate();
    } else if (s == 'p') {
      break;
    } else if (s == 'e') {
      hasFloat = 1;
    }
    if (running) {
      myservo.write(90);
      if (hasFloat) {
        String f = Serial.readStringUntil('\n');
        error = f.toFloat();
        Serial.print("Error is: ");
        Serial.println(error);
        tracking(error);
        hasFloat = 0;
        delay(500);
      } else {
        distance = ultrasonic.read();
        MotorWriting(0, 0);
      }
    }
  }
  MotorWriting(0, 0);
}

void Processing() {
}