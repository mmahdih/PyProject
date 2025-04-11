import serial
import time
import ttkbootstrap as ttk

# Connect to Arduino through the appropriate COM port
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
time.sleep(2)  # Allow time for Arduino to reset and establish communication



# Create the main window
main_window = ttk.Window(themename="darkly")
main_window.title("LED Control")


light_state = 0
arduino.write(b'0')


# Create a frame to hold the buttons
button_frame = ttk.Frame(main_window)
button_frame.pack()

turnonImage = ttk.PhotoImage(file="lightsOn.png")
turnoffImage = ttk.PhotoImage(file="lightsOff.png")


switch_button = ttk.Button(button_frame, style="Link")


def lighton():
    arduino.write(b'1')
    switch_button.configure(image=turnoffImage, command=lightoff)

def lightoff():
    arduino.write(b'0')
    switch_button.configure(image=turnonImage, command=lighton)


# Create buttons to control the LED
if light_state == 0:
    switch_button.configure(image=turnonImage, command=lighton)
    light_state = 1
else:
    switch_button.configure(image=turnoffImage, command=lightoff)
    light_state = 0


switch_button.grid(row=0, column=0, padx=10, pady=10)

# Main event loop
main_window.mainloop()



arduino.close()