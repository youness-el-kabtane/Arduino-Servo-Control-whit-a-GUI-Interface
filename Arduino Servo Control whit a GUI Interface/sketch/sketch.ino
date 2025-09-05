#include <Servo.h>

Servo servoA, servoB, servoC, servoD;

int currentAngle[4] = {90, 90, 90, 90}; // Start at mid-point

void setup() {
  Serial.begin(9600);
  servoA.attach(13); 
  servoB.attach(12);
  servoC.attach(11);
  servoD.attach(10);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    if (data.length() > 0) {
      char id = data.charAt(0);      // A, B, C, or D
      int sep = data.indexOf(':');
      int sep2 = data.indexOf(':', sep + 1);

      if (sep != -1 && sep2 != -1) {
        int target = data.substring(sep + 1, sep2).toInt();
        int speed = data.substring(sep2 + 1).toInt(); // speed: 1 = fast, 10 = slow

        int index = id - 'A';
        Servo* servos[] = {&servoA, &servoB, &servoC, &servoD};

        // Move step-by-step for smooth motion
        int current = currentAngle[index];
        int stepDir = (target > current) ? 1 : -1;

        for (int pos = current; pos != target; pos += stepDir) {
          servos[index]->write(pos);
          delay(speed);  // delay controls speed
        }

        servos[index]->write(target);
        currentAngle[index] = target;
      }
    }
  }
}
