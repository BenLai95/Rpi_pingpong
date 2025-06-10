#include <Ultrasonic.h>
#include <Servo.h>
#include "track.h"
Servo myservo;  // 建立一個 servo 物件，最多可建立 12個 servo
int pos = 180;  // 設定 Servo 位置的變數
#include <Wire.h>
#define ARDUINO_ADDR 0x8

float error = 0;
byte buf[8];
bool hasFloat = false;

Ultrasonic ultrasonic(22, 23);
int distance;

String serialInput = "";

void setup() {
  myservo.attach(24);
  myservo.write(90);
  Serial.begin(9600);
  Wire.begin(ARDUINO_ADDR);
  Wire.onReceive(receiveEvent);
  //Wire.onRequest(requestEvent);  // 新增請求處理函數
}

void loop() {
  // 更新距離數據
  distance = ultrasonic.read();
  if (hasFloat) {
    // 收到新的 float 存放在 error
    Serial.print("Recv float: ");
    Serial.println(error);
    hasFloat = false;
  }
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
  tracking(error);
  if(buf[0]=='n'){
    error = 0;
    Rotate();
  }
}

void receiveEvent(int nbyte) {
  if (hasFloat) {
      union { byte b[4]; float f; } u;
      for (int i = 0; i < 4; i++) {
        u.b[i] = Wire.read();
      }
      error = u.f;
      hasFloat = false;
  }
  else{
    buf[nbyte] = 0;
    for(int i=0;i<nbyte;i++){
      buf[i] = Wire.read();
    }
  }
}



// 修改回傳函數
/*void requestEvent() {
    String data;
    if (serialInput != "") {
        // 如果有序列埠輸入，回傳該輸入
        data = "S:" + serialInput;
    } else {
        // 否則回傳距離數據
        data = "D:" + String(distance);
    }
    Wire.write(data.c_str(), data.length());

}*/