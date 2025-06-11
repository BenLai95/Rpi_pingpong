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
  MotorWriting(0,0);
  Serial2.write('r');
  if(Serial2.available()){
    char s = Serial2.read();
    if(s == 'e'){
      hasFloat = 1;
    }
    else if(s == 'n'){
      error = 0;
      hasFloat = 0;
      Rotate();
    }
    else if(s == 'p'){
      return;
    }
  }
  if (hasFloat) {
    if (Serial2.available()) {
      String f = Serial2.readStringUntil('\n');
      error = f.toFloat();
      String r = Serial2.readStringUntil('\n');
      int radius = r.toInt();
      Serial.print("Error is: ");
      Serial.println(error);
      if(abs(error) < 0.5 && radius < 50){
        MotorWriting(Tp, Tp);
      }else if(abs(error) >= 0.5 && radius < 50){
        error_rotating(error);  // 使用 error 來調整伺服馬達
      }else if(radius >= 50){
        distance = ultrasonic.read();//寫到這邊還沒寫完
        if(distance<=10 || distance>=30){
          MotorWriting(70,70);
        }else{
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
        }
        hasFloat = false;
      }
    }
  }
  MotorWriting(0,0);
}


void Processing() {
}