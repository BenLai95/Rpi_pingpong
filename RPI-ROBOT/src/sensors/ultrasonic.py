class UltrasonicSensor:
    def __init__(self, trigger_pin=3, echo_pin=2):
        import RPi.GPIO as GPIO
        import time
        
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def get_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        elapsed_time = stop_time - start_time
        distance = (elapsed_time * 34300) / 2  # Distance in cm
        return distance

    def cleanup(self):
        import RPi.GPIO as GPIO
        GPIO.cleanup()