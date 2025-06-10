#include <Ultrasonic.h>
#include <Servo.h>
Servo myservo; // 建立一個 servo 物件，最多可建立 12個 servo
int pos = 180;   // 設定 Servo 位置的變數
#include <Wire.h>
#define ARDUINO_ADDR 0x8
char buf[128];

Ultrasonic ultrasonic(22, 23);
int distance;

String serialInput = "";

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
            serialInput.trim();
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


// 修改回傳函數
void requestEvent() {
    // 檢查並傳送序列埠輸入
    if (serialInput.length() > 0) {
        // 印出除錯資訊
        Serial.print("Sending: ");
        Serial.println(serialInput);
        
        // 傳送資料
        Wire.write(serialInput.c_str());
    } else {
        // 如果沒有輸入，傳送空值標記
        Wire.write("NONE", 4);
    }
}