/*
本程式為SR04超音波感測器的範例

首先要安裝ErickSimoes/Ultrasonic的函式庫
VCC接5V，GND接地。Trig接到pin 22，Echo接到pin 23。

HC-SR04賣場：
https://www.jmaker.com.tw/products/sr04

粉絲團：
https://www.facebook.com/jasonshow

傑森創工購物網：https://www.jmaker.com.tw/
傑森創工部落格：https://blog.jmaker.com.tw/
*/
#include <Ultrasonic.h>
#include <Servo.h>
Servo myservo; // 建立一個 servo 物件，最多可建立 12個 servo
int pos = 180;   // 設定 Servo 位置的變數
#include <Wire.h>
#define ARDUINO_ADDR 0x8
char buf[128];

Ultrasonic ultrasonic(22, 23);
int distance;

void setup() { 
    myservo.attach(24);
    myservo.write(180);
    Serial.begin(9600);
    Wire.begin(ARDUINO_ADDR);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);  // 新增請求處理函數
}

void loop() {
    // 更新距離數據
    distance = ultrasonic.read();
    
    // 檢查序列埠是否有資料
    while (Serial.available() > 0) {
        char c = Serial.read();
        if (c == '\n') {
            // 收到完整一行，更新回傳資料
            serialInput = serialInput.trim();  // 移除多餘空白
            Serial.print("收到輸入: ");
            Serial.println(serialInput);
        } else {
            serialInput += c;
        }
    }
    
    delay(100);
}

void receiveEvent(int nbyte) {
    buf[nbyte] = 0;
    for (int i = 0; Wire.available(); i++) {
        buf[i] = Wire.read();
    }
    Serial.println(buf);
}

// 新增全域變數
String serialInput = "";

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