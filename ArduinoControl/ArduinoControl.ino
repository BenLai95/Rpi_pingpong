#include <Ultrasonic.h>
#include <Servo.h>
#include "track.h"
Servo myservo;  // 建立一個 servo 物件，最多可建立 12個 servo
int pos = 180;  // 設定 Servo 位置的變數
#include <Wire.h>
#define ARDUINO_ADDR 0x8

float error = 0;
char buf[128];
bool hasFloat = false;
bool running = false;

Ultrasonic ultrasonic(22, 23);
int distance;

String serialInput = "";

void setup() {
  myservo.attach(24);
  myservo.write(90);
  Serial.begin(9600);
  Wire.begin(ARDUINO_ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);  // 新增請求處理函數
}

void loop() {
  // 檢查序列埠是否有資料
  /*while (Serial.available() > 0) {
        char c = Serial.read();
        if (c == '\n') {
            // 收到完整一行，更新回傳資料
            serialInput.trim();
            Serial.print("收到輸入: ");
            Serial.println(serialInput);
        } else {
            serialInput += c;
        }
    }*/

  /*while (running) {
    distance = ultrasonic.read();
    tracking(error);
    if (buf[0] == 'n') {
      error = 0;
      Rotate();
    }
  }*/
}
int n = 0;
void receiveEvent(int nbyte) {
  if (hasFloat) {
    union {
      byte b[4];
      float f;
    } u;
    for (int i = 0; i < 4; i++) {
      if (i == 0) {
        int k = Wire.read();
      }
      u.b[i] = Wire.read();
      Serial.print("Float byte is ");
      Serial.println(int(u.b[i]));
    }
    error = u.f;
    hasFloat = false;
  } else {
    buf[nbyte] = 0;
    for (int i = 0; i < nbyte; i++) {
      buf[i] = Wire.read();
      Serial.print("Buf byte is ");
      Serial.println(int(buf[i]));
    }
    if (buf[0] == 'e') {
      hasFloat = true;
    }
    if (buf[0] == 's') {
      running = true;
    }
    if (buf[0] == 'p') {
      running = false;
    }
    Serial.print("Buf is ");
    Serial.println(error);
    Serial.println(buf);
    Serial.println(n);
    n++;
  }
}



// 修改回傳函數
void requestEvent() {
    String data;
    if (serialInput != "") {
        // 如果有序列埠輸入，回傳該輸入
        data = "S:" + serialInput;
    } else {
        // 否則回傳距離數據
        data = "D:" + String(distance);
    }
    Wire.write(data.c_str(), data.length());

}