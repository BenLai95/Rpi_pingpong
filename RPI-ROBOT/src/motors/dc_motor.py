class DCMotor:
    def __init__(self, pin_forward, pin_backward):
        import RPi.GPIO as GPIO
        self.pin_forward = pin_forward
        self.pin_backward = pin_backward
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_forward, GPIO.OUT)
        GPIO.setup(self.pin_backward, GPIO.OUT)
        self.pwm_forward = GPIO.PWM(self.pin_forward, 100)
        self.pwm_backward = GPIO.PWM(self.pin_backward, 100)
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)

    def start(self):
        self.pwm_forward.start(100)

    def stop(self):
        self.pwm_forward.stop()
        self.pwm_backward.stop()

    def set_speed(self, speed):
        if speed > 0:
            self.pwm_forward.ChangeDutyCycle(speed)
            self.pwm_backward.ChangeDutyCycle(0)
        elif speed < 0:
            self.pwm_backward.ChangeDutyCycle(-speed)
            self.pwm_forward.ChangeDutyCycle(0)
        else:
            self.stop()