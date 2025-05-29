import time
from motors.servo import ServoMotor
from motors.dc_motor import DCMotor
from sensors.ultrasonic import UltrasonicSensor

def main():
    # Initialize motors and sensors
    servo = ServoMotor(pin=18)  # Example GPIO pin for servo
    dc_motor = DCMotor(pin=23)  # Example GPIO pin for DC motor
    ultrasonic_sensor = UltrasonicSensor(trigger_pin=24, echo_pin=25)  # Example GPIO pins for ultrasonic sensor

    try:
        while True:
            # Get distance from ultrasonic sensor
            distance = ultrasonic_sensor.get_distance()
            print(f"Distance: {distance} cm")

            # Control servo motor based on distance
            if distance < 20:
                servo.set_angle(90)  # Move servo to 90 degrees if object is close
            else:
                servo.set_angle(0)   # Move servo to 0 degrees otherwise

            # Control DC motor based on distance
            if distance < 10:
                dc_motor.set_speed(0)  # Stop motor if object is very close
            else:
                dc_motor.set_speed(100)  # Set motor speed to 100 if object is further away

            time.sleep(1)  # Delay for a second

    except KeyboardInterrupt:
        # Stop motors on exit
        dc_motor.stop()
        print("Program terminated.")

if __name__ == "__main__":
    main()