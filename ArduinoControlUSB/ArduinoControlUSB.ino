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
  myservo.write(170);
}

void loop() {
  while (Serial.available()) {
    char s = Serial.read();
    if (s == 's') {
      running = 1;
    }
    while (running) {
      myservo.write(90);
      if (hasFloat) {
        String f = Serial.readStringUntil('\n');
        error = f.toFloat();
        hasFloat = 0;
      } else {
        distance = ultrasonic.read();
        tracking(error);
        if (s == 'n') {
          error = 0;
          Rotate();
        }
        if (s == 'p') {
          running = 0;
        } else if (s == 'e') {
          hasFloat = 1;
        }
      }
    }
  }
  MotorWriting(0, 0);
}