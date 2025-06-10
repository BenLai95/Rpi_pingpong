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

Ultrasonic ultrasonic(22, 23);
int distance;

void setup()
{ 
  myservo.attach(24);
  myservo.write(180);
  Serial.begin(9600);
  Serial2.begin(9600);
}


void loop() {
  int distance = ultrasonic.read();
  if(Serial2.available()){
    String cmd = Serial2.readStringUntil('\n');
    Serial.print(cmd);
    Serial.println("\nWrited");
  }

}