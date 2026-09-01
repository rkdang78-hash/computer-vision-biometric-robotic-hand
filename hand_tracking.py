import serial
import time
import cv2
import mediapipe as mp
import math

# Change COM3 to your actual port
arduino = serial.Serial('COM4', 9600)
time.sleep(2)
print("Connected to Arduino")

# Setup mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

class Smoother:
    def __init__(self, size=7):
        self.history = []
        self.size = size
    
    def smooth(self, angles):
        self.history.append(angles)
        if len(self.history) > self.size:
            self.history.pop(0)
        smoothed = []
        for i in range(len(angles)):
            avg = sum(h[i] for h in self.history) / len(self.history)
            smoothed.append(int(avg))
        return smoothed

def send_angles(angles):
    data = ','.join(str(int(a)) for a in angles) + '\n'
    arduino.write(data.encode())

def get_distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x)**2 +
        (p1.y - p2.y)**2 +
        (p1.z - p2.z)**2
    )

def get_hand_scale(landmarks):
    wrist = landmarks[0]
    mid_base = landmarks[9]
    return get_distance(wrist, mid_base)

def normalize(distance, min_distance, max_distance):
    normalized = (distance - min_distance) / (max_distance - min_distance)
    return max(0, min(1, normalized))

def to_angle(normalized_distance):
    return (1 - normalized_distance) * 180

def get_all_angles(landmarks):
    angles = []
    scale = get_hand_scale(landmarks)

    for finger, (tip_id, base_id) in finger_pairs.items():
        tip  = landmarks[tip_id]
        base = landmarks[base_id]
        dist = get_distance(tip, base)
        relative_dist = dist / scale
        norm = normalize(relative_dist, finger_min[finger], finger_max[finger])
        angle = to_angle(norm)
        angles.append(angle)

    return angles

finger_pairs = {
    "thumb":  (4, 5),
    "index":  (8, 5),
    "middle": (12, 9),
    "ring":   (16, 13),
    "pinky":  (20, 17),
}

finger_max = {
    "thumb":  0.7260,
    "index":  0.8515,
    "middle": 0.9379,
    "ring":   0.8,
    "pinky":  0.65,
}

finger_min = {
    "thumb":  0.2013,
    "index":  0.3214,
    "middle": 0.2909,
    "ring":   0.2562,
    "pinky":  0.2065,
}

smoother = Smoother(size=7)

cap = cv2.VideoCapture(0)
print("Camera started — press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not found")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            angles = get_all_angles(hand_landmarks.landmark)
            angles = smoother.smooth(angles)
            send_angles(angles)

            print(
                f"Thumb: {angles[0]:3.0f}°  "
                f"Index: {angles[1]:3.0f}°  "
                f"Middle: {angles[2]:3.0f}°  "
                f"Ring: {angles[3]:3.0f}°  "
                f"Pinky: {angles[4]:3.0f}°"
            )

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
