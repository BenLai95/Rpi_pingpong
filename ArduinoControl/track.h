/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		[Code used for tracking]
// Functions  [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

/*===========================import variable===========================*/

#ifndef TRACK_H
#define TRACK_H
int Tp;
double error = 0;
#define MotorR_I1 3    // 定義 A1 接腳（右）
#define MotorR_I2 2    // 定義 A2 接腳（右）
#define MotorR_PWMR 11 // 定義 ENA (PWM調速) 接腳
#define MotorL_I3 6    // 定義 B1 接腳（左）
#define MotorL_I4 5    // 定義 B2 接腳（左）
#define MotorL_PWML 12 // 定義 ENB (PWM調速) 接腳
/*===========================import variable===========================*/

// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
  // TODO: use TB6612 to control motor voltage & direction
  if (vR >= 0) {
    digitalWrite(MotorR_I1, LOW);
    digitalWrite(MotorR_I2, HIGH);
  } else {
    digitalWrite(MotorR_I1, HIGH);
    digitalWrite(MotorR_I2, LOW);
    vR = -vR;
  }
  if (vL >= 0) {
    digitalWrite(MotorL_I3, LOW);
    digitalWrite(MotorL_I4, HIGH);
  } else {
    digitalWrite(MotorL_I3, HIGH);
    digitalWrite(MotorL_I4, LOW);
    vL = -vL;
  }
  analogWrite(MotorL_PWML, vL);
  analogWrite(MotorR_PWMR, vR);
}  // MotorWriting

// Handle negative motor_PWMR value.

// P/PID control Tracking
void tracking() {
  
}  // tracking

#endif  // TRACK_H
