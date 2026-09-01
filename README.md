# computer-vision-biometric-robotic-hand

A real-time robotic hand that mirrors human hand movements using computer vision and servo control.

## Demo Prototype

https://github.com/user-attachments/assets/25cb12b8-40ed-42f7-a7ef-f748055aacc3

## How It Works
To put it simply, I used MediaPipe to process the camera feed and detect the landmarks(joints) across my hand in real time. Every frame captured by the camera, the program records the position of each landmark and calculates the distance between the tip of each finger and its base knuckle. By comparing that distance to the maximum distance when the finger is fully extended, the program determines what angle the corresponding servo motor should be at. A curled finger brings the tip close to the base resulting in a small distance and a high servo angle, while a fully extended finger maximizes that distance and keeps the servo at a low angle. Those angles are then sent from the Python script to the Arduino over serial communication, which drives the servo motors on the robotic hand to mirror my finger positions in real time.

## Hardware
- Arduino Uno
- PCA9685 Servo Driver
- 5x MG90S Servos
- Webcam
- Bench power supply
- Breadboard and wiring

## Wiring
<img width="911" height="672" alt="image" src="https://github.com/user-attachments/assets/4aac1e7b-d4ae-4b59-a1ab-6ac757a5015d" />


## Software
- Python 3.11
- MediaPipe
- OpenCV
- PySerial

## Installation
- Clone the repository

    git clone https://github.com/yourusername/computer-vision-robotic-hand
    cd computer-vision-robotic-hand

- Install Python dependencies

    pip install mediapipe opencv-python pyserial

- Upload Arduino sketch

    Open arduino/servo_control.ino in Arduino IDE
    Select board: Tools → Board → Arduino Uno
    Select port: Tools → Port → COM# (your port)
    Click upload

- Hardware setup

    Wire PCA9685 to Arduino (VCC→5V, GND→GND, SDA→A4, SCL→A5)
    Connect servos to PCA9685 channels 0-4
    Connect power supply to PCA9685 terminal block (5V, 5A)
    Connect webcam to computer

- Configure serial port

    Open python/hand_tracking.py
    Change COM4 to your Arduino's COM port:
    python
    arduino = serial.Serial('COM4', 9600)

- Run

    py -3.11 python/hand_tracking.py
    Calibration Note

    Everyone's hand is slightly different so you may need to calibrate the finger distance values. Instructions in docs/calibration.md



## Future Improvements
- Make a custom pcb to clean up the breadboard mess and make it less prone to error from loose wiring
- Implement 3 point angle calculation for better accuracy for finger tracking
