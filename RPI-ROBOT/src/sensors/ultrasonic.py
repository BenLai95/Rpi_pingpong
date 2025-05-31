import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin=3, echo_pin=2):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        # Initialize trigger pin to LOW
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.1)  # Let sensor settle
        
    def get_distance(self):
        """
        Get distance measurement in centimeters
        Returns -1 if timeout occurs
        """
        # Ensure trigger pin is LOW
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.0002)  # 0.2ms

        # Send 10us pulse
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)  # 10us
        GPIO.output(self.trigger_pin, False)

        # Wait for echo to go HIGH (start of pulse)
        pulse_start = time.time()
        timeout_start = pulse_start + 0.02  # 20ms timeout
        
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
            if pulse_start > timeout_start:
                return -1  # Timeout waiting for echo start

        # Wait for echo to go LOW (end of pulse)
        pulse_end = time.time()
        timeout_end = pulse_end + 0.02  # 20ms timeout
        
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
            if pulse_end > timeout_end:
                return -1  # Timeout waiting for echo end

        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        # Speed of sound = 34300 cm/s
        # Distance = (Time × Speed) / 2 (divide by 2 for round trip)
        distance = (pulse_duration * 34300) / 2
        
        # Filter out unrealistic readings
        if distance < 2 or distance > 400:  # HC-SR04 typical range: 2-400cm
            return -1
            
        return round(distance, 2)
    
    def get_average_distance(self, samples=3, delay=0.1):
        """
        Get average distance over multiple samples for better accuracy
        """
        measurements = []
        
        for _ in range(samples):
            distance = self.get_distance()
            if distance != -1:  # Only include valid measurements
                measurements.append(distance)
            time.sleep(delay)
        
        if not measurements:
            return -1  # No valid measurements
            
        return round(sum(measurements) / len(measurements), 2)
    
    def is_object_detected(self, threshold_cm=20):
        """
        Simple object detection within threshold distance
        """
        distance = self.get_distance()
        return distance != -1 and distance <= threshold_cm
    
    def cleanup(self):
        """Clean up GPIO resources"""
        GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    sensor = UltrasonicSensor(trigger_pin=3, echo_pin=2)
    
    try:
        while True:
            # Single measurement
            distance = sensor.get_distance()
            
            if distance == -1:
                print("Measurement failed (timeout or out of range)")
            else:
                print(f"Distance: {distance} cm")
            
            # Average measurement (more accurate)
            avg_distance = sensor.get_average_distance(samples=5)
            if avg_distance != -1:
                print(f"Average distance: {avg_distance} cm")
            
            # Object detection
            if sensor.is_object_detected(threshold_cm=30):
                print("Object detected within 30cm!")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        sensor.cleanup()