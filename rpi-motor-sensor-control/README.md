# rpi-motor-sensor-control

This project is designed to control a servo motor, a DC motor, and an ultrasonic sensor using a Raspberry Pi. It provides a simple interface to interact with these components, making it suitable for various robotics and automation projects.

## Project Structure

```
rpi-motor-sensor-control
├── src
│   ├── main.py          # Entry point of the application
│   ├── motors
│   │   ├── servo.py     # Controls the servo motor
│   │   └── dc_motor.py  # Controls the DC motor
│   ├── sensors
│   │   └── ultrasonic.py # Interfaces with the ultrasonic sensor
│   └── utils
│       └── __init__.py  # Utility functions and constants
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rpi-motor-sensor-control
   ```

2. **Install the required dependencies:**
   Make sure you have Python and pip installed on your Raspberry Pi. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Connect the hardware:**
   - Connect the servo motor, DC motor, and ultrasonic sensor to the appropriate GPIO pins on the Raspberry Pi as specified in the code.

## Usage

1. **Run the application:**
   Execute the main script to start the application:
   ```bash
   python src/main.py
   ```

2. **Control the motors and read sensor data:**
   Follow the prompts in the terminal to control the motors and read distances from the ultrasonic sensor.

## Example

- To set the servo motor to a specific angle, you can use the `set_angle(angle)` method from the `ServoMotor` class.
- To start the DC motor, call the `start()` method from the `DCMotor` class, and adjust its speed using `set_speed(speed)`.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Your feedback and improvements are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.