#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 600
#define NUM_SERVOS 5

void setServoAngle(uint8_t channel, int angle) {
    angle = constrain(angle, 0, 180);
    int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
    pwm.setPWM(channel, 0, pulse);
}

void setup() {
    Serial.begin(9600);
    pwm.begin();
    pwm.setPWMFreq(60);
    delay(10);
    Serial.println("Arduino ready");
}

void loop() {
    if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');

        int angles[NUM_SERVOS];
        int index = 0;
        char buf[64];
        data.toCharArray(buf, 64);
        char* token = strtok(buf, ",");

        while (token != NULL && index < NUM_SERVOS) {
            angles[index] = atoi(token);
            token = strtok(NULL, ",");
            index++;
        }

        for (int i = 0; i < NUM_SERVOS; i++) {
            setServoAngle(i, angles[i]);
        }
    }
}
