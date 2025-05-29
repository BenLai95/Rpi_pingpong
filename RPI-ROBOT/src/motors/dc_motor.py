import RPi.GPIO as GPIO
import time

class DCMotor:
    def __init__(self, pwm_pin, in1_pin, in2_pin):
        self.pwm_pin = pwm_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pwm_pin, 1000)  # 1kHz PWM
        self.pwm.start(0)

    def set_speed(self, speed):
        """
        speed: -100 ~ 100
        正數為正轉，負數為反轉，0為停止
        """
        if speed > 0:
            GPIO.output(self.in1_pin, GPIO.HIGH)
            GPIO.output(self.in2_pin, GPIO.LOW)
            self.pwm.ChangeDutyCycle(min(speed, 100))
        elif speed < 0:
            GPIO.output(self.in1_pin, GPIO.LOW)
            GPIO.output(self.in2_pin, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(min(-speed, 100))
        else:
            GPIO.output(self.in1_pin, GPIO.LOW)
            GPIO.output(self.in2_pin, GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)

    def stop(self):
        self.set_speed(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

class CarController:
    def __init__(self):
        # A馬達：PWMA=13, AIN1=26, AIN2=19
        # B馬達：PWMB=16, BIN1=21, BIN2=20
        self.motorA = DCMotor(pwm_pin=13, in1_pin=26, in2_pin=19)
        self.motorB = DCMotor(pwm_pin=16, in1_pin=21, in2_pin=20)

    def forward(self, speed=80):
        self.motorA.set_speed(speed)
        self.motorB.set_speed(speed)

    def backward(self, speed=80):
        self.motorA.set_speed(-speed)
        self.motorB.set_speed(-speed)

    def left(self, speed=80):
        self.motorA.set_speed(-speed)
        self.motorB.set_speed(speed)

    def right(self, speed=80):
        self.motorA.set_speed(speed)
        self.motorB.set_speed(-speed)

    def stop(self):
        self.motorA.stop()
        self.motorB.stop()

    def cleanup(self):
        self.motorA.cleanup()
        self.motorB.cleanup()