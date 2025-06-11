#include "track.h"
#include <Servo.h>
Servo myservo;

void setup() {
  // put your setup code here, to run once:
  MotorWriting(150, 150);
  myservo.attach(24);
  myservo.write(170);

}

void loop() {
  // put your main code here, to run repeatedly:

}
