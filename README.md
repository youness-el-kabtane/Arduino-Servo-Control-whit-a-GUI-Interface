
# Arduino Servo Control whit a GUI Interface

> The entire system is simulated in Proteus Design Suite 

This project implements a 4-servo motor control system, where each motor’s angle and speed are adjustable in real time. The servos are connected to an Arduino board, which communicates via USB with a Python-based dashboard, providing an intuitive interface for precise motor control. The system demonstrates seamless hardware-software integration for applications in robotics and automation.

![ image](https://github.com/youness-el-kabtane/Arduino-Servo-Control-whit-a-GUI-Interface/blob/main/image/image1.png?raw=true)

## Hardware Components:

-   **Arduino Board** 
-   **4 Servo Motors** (standard or digital, depending on torque requirements)

## Basics of Serial Communication

-   **Serial communication** sends data **one bit at a time** over a single wire (TX for transmit, RX for receive).
    
-   Standard communication uses parameters like:
    
    -   **Baud rate**: Speed of data transfer (bits per second). In your project: `9600 bps`.
    -   **Start bit**: Signals the beginning of data.
    -   **Data bits**: Usually 8 bits per character.     
    -   **Stop bit**: Signals the end of data.
    
-   Arduino’s USB port emulates a **virtual COM port** on the PC, allowing serial communication through USB.

## Step-by-Step Guide to Simulate Virtual Serial Ports in Proteus Using VSPE

### Step 1: Install VSPE

1.  Download **VSPE (Virtual Serial Port Emulator)** from the official website.
2.  Install it on your Windows PC.
3.  Run **VSPE**

### Step 2: Create a Pair of Virtual COM Ports

- In VSPE, click on **“Create new device”**.

![enter image description here](https://github.com/youness-el-kabtane/Arduino-Servo-Control-whit-a-GUI-Interface/blob/main/image/Screenshot%201.png?raw=true)

- Choose Virtual Pair

![enter image description here](https://github.com/youness-el-kabtane/Arduino-Servo-Control-whit-a-GUI-Interface/blob/main/image/Screenshot%202.png?raw=true)

- Make your Costume Virtual COM Port 

![enter image description here](https://github.com/youness-el-kabtane/Arduino-Servo-Control-whit-a-GUI-Interface/blob/main/image/Screenshot%203.png?raw=true)

- On Proteus search **COMPIM** , In parameter choose your 1st Port

![enter image description here](https://github.com/youness-el-kabtane/Arduino-Servo-Control-whit-a-GUI-Interface/blob/main/image/Screenshot%204.png?raw=true)

## Arduino Script Explain

### 1. Include Library and Define Servo Objects

```Cpp
#include <Servo.h>

Servo servoA, servoB, servoC, servoD;
```

-   `#include <Servo.h>`: Includes the Arduino Servo library, which provides functions to control servo motors.
-   `Servo servoA, servoB, servoC, servoD;`: Creates four servo objects to represent each motor.

### 2.Current Angle Array

```Cpp
int currentAngle[4] = {90, 90, 90, 90}; // Start at mid-point
```

-   Stores the current angles of the 4 servos.
-   Initialized to `90°`, which is typically the middle position for standard servos.

### 3.Setup Function

```Cpp
void setup() {
  Serial.begin(9600);
  servoA.attach(13); 
  servoB.attach(12);
  servoC.attach(11);
  servoD.attach(10);
}
```
-   `Serial.begin(9600);`: Starts serial communication at 9600 baud to communicate with the Python dashboard.
-   `servoX.attach(pin);`: Links each servo object to a specific Arduino digital pin (10–13 in this case).

### 4.Loop Function

```Cpp
void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();
```
-   `Serial.available()`: Checks if there is data sent from the Python program.
-   `Serial.readStringUntil('\n')`: Reads the incoming data until a newline character is received.
-   `data.trim()`: Removes any leading or trailing whitespace.

### 5.Parsing the Command

```Cpp
if (data.length() > 0) {
  char id = data.charAt(0);      // A, B, C, or D
  int sep = data.indexOf(':');
  int sep2 = data.indexOf(':', sep + 1);

  if (sep != -1 && sep2 != -1) {
    int target = data.substring(sep + 1, sep2).toInt();
    int speed = data.substring(sep2 + 1).toInt(); // speed: 1 = fast, 10 = slow
```
-   The Python program sends a command in the format: `A:90:5`
    -   `A` → servo ID
    -   `90` → target angle
    -   `5` → speed
-   The code finds the positions of the colons (`:`) to separate the values.
-   `substring()` extracts the target angle and speed and converts them to integers.

### 6.Mapping Servo Object

```Cpp
int index = id - 'A';
Servo* servos[] = {&servoA, &servoB, &servoC, &servoD};
```

-   Converts the character `A/B/C/D` to an array index `0–3`.
-   Stores pointers to all servo objects in an array for easy access.

### 7.Smooth Movement

```Cpp
int current = currentAngle[index];
int stepDir = (target > current) ? 1 : -1;

for (int pos = current; pos != target; pos += stepDir) {
  servos[index]->write(pos);
  delay(speed);  // delay controls speed
}

servos[index]->write(target);
currentAngle[index] = target;
```
-   `stepDir`: Determines the direction to move (increasing or decreasing angle).
-   `for` loop moves the servo one degree at a time from the current angle to the target angle.
-   `delay(speed)`: Controls how fast the servo moves; smaller numbers → faster movement.
-   After movement, it updates `currentAngle[index]` so the next command knows the current position.

## Essential Python Tkinter dashboard program

![enter image description here](https://github.com/youness-el-kabtane/Arduino-Servo-Control-whit-a-GUI-Interface/blob/main/image/image3.png?raw=true)

-   The dashboard controls 4 servo motors (Servo 1-4) arranged in a grid layout
-   Each servo has a unique identifier (ID: A, B, C, D respectively)
-   There's a connection panel at the top right showing "Disconnected" status with port selection and connect/disconnect buttons

### 1.Import Libraries

```py
import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
```

### 2.Serial Connection Functions

```py
arduino = None

def connect_serial():
    global arduino
    port = port_var.get()
    try:
        arduino = serial.Serial(port, 9600, timeout=1)
        status_label.config(text=f"Connected to {port}", foreground="#4CAF50")
        connection_indicator.config(bg="#4CAF50")
    except:
        status_label.config(text="Disconnected", foreground="#F44336")
        connection_indicator.config(bg="#F44336")

def disconnect_serial():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        status_label.config(text="Disconnected", foreground="#F44336")
        connection_indicator.config(bg="#F44336")
```

-   `arduino`: Global variable to hold the serial connection.
-   `connect_serial()`: Opens a serial connection with the selected port at 9600 baud. Updates status text and indicator color (`green` for connected, `red` for disconnected).
-   `disconnect_serial()`: Closes the serial connection and updates status.

### 3.Sending Servo Commands

```py
def send_servo_command(motor_id, angle, speed):
    if arduino and arduino.is_open:
        command = f"{motor_id}:{angle}:{speed}\n"
        arduino.write(command.encode())
```

-   Formats commands like `A:90:5\n` for Arduino.
-   Sends the command via serial to control servo ID, angle, and speed.

### 4.Create Servo Control Panel

```py
def create_servo_control(title, motor_id, row, col):
    servo_frame = tk.Frame(controls_frame, bg="#FFFFFF", relief="flat", bd=0, padx=10, pady=10)
    servo_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    title_frame = tk.Frame(servo_frame, bg="#FFFFFF")
    title_frame.pack(fill="x", pady=(0, 10))

    tk.Label(title_frame, text=title, font=("Helvetica", 12, "bold"),
             fg="#333333", bg="#FFFFFF").pack(side="left")

    tk.Label(title_frame, text=f"ID: {motor_id}", font=("Helvetica", 10),
             fg="#666666", bg="#FFFFFF").pack(side="right")

    angle_var = tk.IntVar(value=90)
    speed_var = tk.IntVar(value=5)

    def update_servo(val=None):
        angle = angle_var.get()
        speed = speed_var.get()
        send_servo_command(motor_id, angle, speed)
        angle_value_label.config(text=f"{angle}°")
        speed_value_label.config(text=f"{speed}ms")

    angle_frame = tk.Frame(servo_frame, bg="#FFFFFF")
    angle_frame.pack(fill="x", pady=(0, 15))

    tk.Label(angle_frame, text="Angle", font=("Helvetica", 10),
             fg="#555555", bg="#FFFFFF").pack(anchor="w")

    angle_value_frame = tk.Frame(angle_frame, bg="#FFFFFF")
    angle_value_frame.pack(fill="x")

    tk.Label(angle_value_frame, text="0°", font=("Helvetica", 8),
             fg="#999999", bg="#FFFFFF").pack(side="left")

    angle_value_label = tk.Label(angle_value_frame, text="90°", font=("Helvetica", 10),
                                 fg="#2196F3", bg="#FFFFFF")
    angle_value_label.pack(side="right")

    angle_scale = tk.Scale(angle_frame, from_=0, to=180, orient=tk.HORIZONTAL,
                           variable=angle_var, command=lambda val: update_servo(),
                           bg="#FFFFFF", fg="#333333", highlightthickness=0,
                           troughcolor="#E0E0E0", activebackground="#BBDEFB",
                           length=200, width=12, sliderlength=20)
    angle_scale.pack(fill="x", pady=5)

    tk.Label(angle_frame, text="180°", font=("Helvetica", 8),
             fg="#999999", bg="#FFFFFF").pack(anchor="e")

    speed_frame = tk.Frame(servo_frame, bg="#FFFFFF")
    speed_frame.pack(fill="x")

    tk.Label(speed_frame, text="Speed", font=("Helvetica", 10),
             fg="#555555", bg="#FFFFFF").pack(anchor="w")

    speed_value_frame = tk.Frame(speed_frame, bg="#FFFFFF")
    speed_value_frame.pack(fill="x")

    tk.Label(speed_value_frame, text="Fast", font=("Helvetica", 8),
             fg="#999999", bg="#FFFFFF").pack(side="left")

    speed_value_label = tk.Label(speed_value_frame, text="5ms", font=("Helvetica", 10),
                                 fg="#4CAF50", bg="#FFFFFF")
    speed_value_label.pack(side="right")

    speed_scale = tk.Scale(speed_frame, from_=1, to=20, orient=tk.HORIZONTAL,
                           variable=speed_var, command=lambda val: update_servo(),
                           bg="#FFFFFF", fg="#333333", highlightthickness=0,
                           troughcolor="#E0E0E0", activebackground="#C8E6C9",
                           length=200, width=12, sliderlength=20)
    speed_scale.pack(fill="x", pady=5)

    tk.Label(speed_frame, text="Slow", font=("Helvetica", 8),
             fg="#999999", bg="#FFFFFF").pack(anchor="e")
```
This function builds a control panel for **each servo**:

#### 4.1 Frame & Title

-   Creates a `Frame` to hold the servo controls
-   Shows the servo name (e.g., "Servo 1") and its ID (A, B, C, D).

#### 4.2 Angle Control

-   Uses a horizontal `Scale` widget to adjust the angle from 0° to 180°.
-   Shows the current value (`angle_value_label`).
-   `update_servo()` is called whenever the slider changes to send the updated command to Arduino.
    
#### 4.3 Speed Control

-   Uses another horizontal `Scale` to adjust speed (1 = fast, 20 = slow).
-   Displays speed label (`speed_value_label`).
-   Also calls `update_servo()` when changed.
    
####  4.4 Smooth Updates

-   Moving the sliders in real-time updates the Arduino servo using `send_servo_command()`.

---
**Author:** Youness El Kabtane

**Website:** [younesselkabtane](https://sites.google.com/view/younesselkabtane/home?authuser=1)

**Version:** 1.0.0

**Made with 💗**
