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
#define MotorR_I1 2    // 定義 A1 接腳（右）
#define MotorR_I2 3    // 定義 A2 接腳（右）
#define MotorR_PWMR 11 // 定義 ENA (PWM調速) 接腳
#define MotorL_I3 5    // 定義 B1 接腳（左）
#define MotorL_I4 6    // 定義 B2 接腳（左）
#define MotorL_PWML 12 // 定義 ENB (PWM調速) 接腳
#include <Ultrasonic.h>
#include <Servo.h>
Servo myservo; // 建立一個 servo 物件，最多可建立 12個 servo
int pos = 0;   // 設定 Servo 位置的變數

Ultrasonic ultrasonic(22, 23);
int distance;

void MotorWriting(double vL, double vR)
{
  // TODO: use TB6612 to control motor voltage & direction
  if (vR >= 0)
  {
    digitalWrite(MotorR_I1, LOW);
    digitalWrite(MotorR_I2, HIGH);
  }
  else
  {
    digitalWrite(MotorR_I1, HIGH);
    digitalWrite(MotorR_I2, LOW);
    vR = -vR;
  }
  if (vL >= 0)
  {
    digitalWrite(MotorL_I3, LOW);
    digitalWrite(MotorL_I4, HIGH);
  }
  else
  {
    digitalWrite(MotorL_I3, HIGH);
    digitalWrite(MotorL_I4, LOW);
    vL = -vL;
  }
  analogWrite(MotorL_PWML, vL);
  analogWrite(MotorR_PWMR, vR);
} // MotorWriting

void setup()
{
  Serial.begin(9600);
  myservo.attach(24);
  Serial1.begin(9600);
}

void loop()
{
  /*
  // 正轉 180度，從 0 度旋轉到 180 度，每次 1 度
  for (pos = 0; pos <= 180; pos += 1)
  {
    myservo.write(pos);    // 告訴 servo 走到 'pos' 的位置
    delay(15);        // 等待 15ms 讓 servo 走到指定位置
  }

  // 反轉 180度，從 180 度旋轉到 0 度，每次 1 度
  for (pos = 180; pos >= 0; pos -= 1)
  {
    myservo.write(pos);   // 告訴 servo 走到 'pos' 的位置

    delay(15);   // 等待 15ms 讓 servo 走到指定位置
  }

  distance = ultrasonic.read(); //不加參數就是輸出CM，可用read(INC)輸出英寸

  Serial.print("Distance in CM: ");
  Serial.println(distance);
  delay(500); //每次間格0.5秒

  MotorWriting(50,50);
  delay(1000);
  MotorWriting(-50,-50);
  delay(1000);
  */
  if (Serial.available()) {
    char c = Serial.read();
    Serial1.write(c);  // 傳給 RPi
  }

  // 如果 RPi 傳資料進來，傳給 Serial Monitor，**不要再寫回 Serial1**
  if (Serial1.available()) {
    char c = Serial1.read();
    Serial.write(c);  // 顯示在 Arduino IDE
  }
}