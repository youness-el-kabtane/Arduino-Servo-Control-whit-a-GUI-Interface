import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

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

def send_servo_command(motor_id, angle, speed):
    if arduino and arduino.is_open:
        command = f"{motor_id}:{angle}:{speed}\n"
        arduino.write(command.encode())

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

root = tk.Tk()
root.title("Servo Control Panel")
root.geometry("1050x450")
root.configure(bg="#F5F5F5")
root.resizable(False, False)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

header_frame = tk.Frame(root, bg="#FFFFFF", height=80, padx=20, pady=10)
header_frame.grid(row=0, column=0, sticky="ew")
header_frame.grid_columnconfigure(1, weight=1)

tk.Label(header_frame, text="Dashboard", font=("Helvetica", 10, "bold"),
         fg="#333333", bg="#FFFFFF").grid(row=0, column=0, sticky="w")

connection_frame = tk.Frame(header_frame, bg="#FFFFFF")
connection_frame.grid(row=0, column=1, sticky="e")

port_frame = tk.Frame(connection_frame, bg="#FFFFFF")
port_frame.pack(side="left", padx=5)

tk.Label(port_frame, text="Port:", font=("Helvetica", 10),
         fg="#555555", bg="#FFFFFF").pack(anchor="w")

ports = [p.device for p in serial.tools.list_ports.comports()]
port_var = tk.StringVar()

style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', fieldbackground="#FFFFFF", background="#FFFFFF",
                foreground="#333333", bordercolor="#E0E0E0", arrowcolor="#333333")

port_menu = ttk.Combobox(port_frame, textvariable=port_var, values=ports,
                         state="readonly", width=15)
port_var.set("Select Port")
port_menu.pack()

button_frame = tk.Frame(connection_frame, bg="#FFFFFF")
button_frame.pack(side="left", padx=10)

connect_btn = tk.Button(button_frame, text="Connect", command=connect_serial,
                        bg="#4CAF50", fg="white", font=("Helvetica", 10),
                        padx=12, pady=2, relief="flat", bd=0)
connect_btn.pack(side="left", padx=2)

disconnect_btn = tk.Button(button_frame, text="Disconnect", command=disconnect_serial,
                           bg="#F44336", fg="white", font=("Helvetica", 10),
                           padx=12, pady=2, relief="flat", bd=0)
disconnect_btn.pack(side="left", padx=2)

status_frame = tk.Frame(connection_frame, bg="#FFFFFF")
status_frame.pack(side="left", padx=10)

connection_indicator = tk.Label(status_frame, text="", font=("Helvetica", 10),
                                fg="white", bg="#F44336", width=2, height=1)
connection_indicator.pack(side="left", padx=(0, 5))

status_label = tk.Label(status_frame, text="Disconnected", font=("Helvetica", 10),
                        fg="#F44336", bg="#FFFFFF")
status_label.pack(side="left")

main_frame = tk.Frame(root, bg="#F5F5F5")
main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)


controls_frame = tk.Frame(main_frame, bg="#F5F5F5")
controls_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

controls_frame.grid_columnconfigure(0, weight=1)
controls_frame.grid_columnconfigure(1, weight=1)
controls_frame.grid_columnconfigure(2, weight=1)
controls_frame.grid_columnconfigure(3, weight=1)
controls_frame.grid_rowconfigure(0, weight=1)

create_servo_control("Servo 1", "A", 0, 0)
create_servo_control("Servo 2", "B", 0, 1)
create_servo_control("Servo 3", "C", 0, 2)
create_servo_control("Servo 4", "D", 0, 3)

footer_frame = tk.Frame(root, bg="#FFFFFF", height=40, padx=20, pady=10)
footer_frame.grid(row=2, column=0, sticky="ew")
footer_frame.grid_columnconfigure(0, weight=1)

tk.Label(footer_frame, text="Servo Control Panel v1.0", font=("Helvetica", 9),
         fg="#999999", bg="#FFFFFF").pack(side="right")

def on_enter(e):
    e.widget['background'] = '#388E3C' if e.widget == connect_btn else '#D32F2F'

def on_leave(e):
    e.widget['background'] = '#4CAF50' if e.widget == connect_btn else '#F44336'

connect_btn.bind("<Enter>", on_enter)
connect_btn.bind("<Leave>", on_leave)
disconnect_btn.bind("<Enter>", on_enter)
disconnect_btn.bind("<Leave>", on_leave)

root.mainloop()
