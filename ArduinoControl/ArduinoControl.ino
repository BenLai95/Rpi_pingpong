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
String remainingInput = "";  // 儲存尚未傳送的資料

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
    String toSend;
    toSend = serialInput;
    Serial.print("toSend =");
    Serial.println(toSend);
    Wire.write(toSend,len(toSend));

    /*if (serialInput.length() > 0 || remainingInput.length() > 0) {
        // 如果有剩餘資料，優先處理
        String toSend;
        if (remainingInput.length() > 0) {
            toSend = remainingInput;
            remainingInput = "";
        } else {
            toSend = serialInput;
            serialInput = "";
        }

        // 如果資料超過31個字元，分次傳送
        if (toSend.length() > 31) {
            // 取前31個字元傳送
            String currentSend = toSend.substring(0, 31);
            // 保存剩餘的字元
            remainingInput = toSend.substring(31);
            
            char buffer[32];
            currentSend.toCharArray(buffer, 32);
            Wire.write((uint8_t*)buffer, 32);
            
            Serial.print("Sending part: ");
            Serial.println(currentSend);
            Serial.print("Remaining: ");
            Serial.println(remainingInput);
        } else {
            // 資料夠短，一次傳完
            char buffer[32];
            toSend.toCharArray(buffer, 32);
            Wire.write((uint8_t*)buffer, 32);
            
            Serial.print("Sending all: ");
            Serial.println(toSend);
        }
    } else {
        // 發送固定長度的空值標記
        char buffer[32] = "NONE";
        Wire.write((uint8_t*)buffer, 32);
    }*/
}