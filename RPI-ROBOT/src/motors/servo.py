class ServoMotor:
    def __init__(self, pin):
        import RPi.GPIO as GPIO
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50 Hz
        self.pwm.start(0)

    def set_angle(self, angle):
        duty_cycle = (angle / 18) + 2
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()