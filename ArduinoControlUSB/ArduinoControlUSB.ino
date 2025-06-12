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
      myservo.write(170);
      break;
    } else if (s == 'e') {
      hasFloat = 1;
    }
    if (running) {
      myservo.write(90);
      if (hasFloat) {
        String f = Serial2.readStringUntil('\n');
        error = f.toFloat();
        String r = Serial2.readStringUntil('\n');
        int radius = r.toInt();
        Serial.print("Error is: ");
        Serial.println(error);
        if (radius < 50) {
          tracking(error);
          hasFloat = 0;
        }
        //else if (radius > 50 && (error < 50||error >150)) {
        else if (radius > 50) {
          MotorWriting(0, 0);
          delay(100);
          while (true) {
            int distance = ultrasonic.read();
            if (distance <= 15) {
              break;
            } else {
              MotorWriting(60, 80);
              delay(50);
            }
          }
          MotorWriting(0, 0);
          myservo.write(120);
          delay(500);
          myservo.write(150);
          delay(500);
          myservo.write(180);
          delay(500);
          myservo.write(150);
          delay(500);
          myservo.write(120);
          delay(500);
          myservo.write(90);
        } /*else if (radius > 50 && error >= 50) {
          MotorWriting(0, 0);
          error_tracking(error);
          hasFloat = 0;
        }*/
      }
    }
  }
  MotorWriting(0, 0);
}

/*void loop() {
  char s = Serial.read();
  if(s == 'u'){
    myservo.write(90);
  }
  else if(s == 'd'){
    myservo.write(150);
    delay(500);
    myservo.write(175);
  }
  Serial.println(ultrasonic.read());
}*/