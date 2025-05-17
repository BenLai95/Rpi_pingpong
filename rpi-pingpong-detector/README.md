# rpi-pingpong-detector

This project is designed for detecting ping pong balls using a Raspberry Pi and its camera. The application captures video frames from the Pi camera and processes them to determine if a ping pong ball is present in the frame.

## Project Structure

```
rpi-pingpong-detector
├── src
│   ├── main.py                # Entry point of the application
│   ├── camera
│   │   └── pi_camera.py       # Handles camera initialization and frame capture
│   ├── detection
│   │   └── pingpong_detector.py # Contains methods for detecting ping pong balls
│   └── utils
│       └── image_utils.py     # Utility functions for image processing
├── requirements.txt           # Lists project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rpi-pingpong-detector
   ```

2. **Install dependencies:**
   Make sure you have Python and pip installed on your Raspberry Pi. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Connect the Pi Camera:**
   Ensure that the Raspberry Pi camera is connected and enabled in the Raspberry Pi configuration settings.

## Usage

To run the application, execute the following command in the terminal:
```bash
python src/main.py
```

The application will start capturing frames from the camera and will output whether a ping pong ball is detected in the frame.

## Functionality

- **Camera Initialization:** The application initializes the Raspberry Pi camera and captures frames.
- **Image Processing:** Captured frames are processed to detect the presence of a ping pong ball using image processing techniques.
- **Detection:** The application provides real-time feedback on whether a ping pong ball is present in the frame.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Your contributions are welcome!