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

## Calibration

- Step 1 — Enable calibration mode

In hand_tracking.py find the get_all_angles function and add this temporary print line after relative_dist is calculated:

python
print(f"{finger}: {relative_dist:.4f}")

- Step 2 — Find your open hand values

Run the script and hold your hand fully open and flat in front of the camera. Note the values printing for each finger, these are your maximum distances.

- Step 3 — Find your closed hand values

Make the tightest fist you can and note the values printing for each finger, these are your minimum distances.

- Step 4 — Update the calibration values

In hand_tracking.py find these dictionaries and replace with your measured values:

python
finger_max = {
    "thumb":  0.7260,  # your open thumb value
    "index":  0.8515,  # your open index value
    "middle": 0.9379,  # your open middle value
    "ring":   0.8,     # your open ring value
    "pinky":  0.65,    # your open pinky value
}

finger_min = {
    "thumb":  0.2013,  # your closed thumb value
    "index":  0.3214,  # your closed index value
    "middle": 0.2909,  # your closed middle value
    "ring":   0.2562,  # your closed ring value
    "pinky":  0.2065,  # your closed pinky value
}

- Step 5 — Remove the temporary print line

Delete the calibration print line you added in Step 1.

- Step 6 — Verify calibration

Run the script and confirm:

Open hand  = all fingers read close to 0°
Tight fist = all fingers read close to 180°

Tips

Keep your hand at a consistent distance from the camera during calibration
Good lighting gives more consistent readings
If a finger feels unresponsive its min and max values are probably too close together — spread them further apart
The thumb is the trickiest finger, if it feels off try adjusting its values independently first

## Results
Photos and videos of it working

## Future Improvements
What you plan to add next
