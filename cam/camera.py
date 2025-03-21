import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Create a Tkinter window
root = tk.Tk()

# Create a label to display the video
label = tk.Label(root)
label.pack()

# Create a button to capture a frame
def capture_frame():
    # Get the current frame
    ret, frame = vc.read()
    # Save the frame to a file
    cv2.imwrite("captured_frame.jpg", frame)

capture_button = tk.Button(root, text="Capture Frame", command=capture_frame)
capture_button.pack()

# Create a button to record video
def record_video():
    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('../html_pages/output.avi', fourcc, 20.0, (640, 480))
    while True:
        ret, frame = vc.read()
        out.write(frame)
        cv2.imshow("preview", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()

record_button = tk.Button(root, text="Record Video", command=record_video)
record_button.pack()

# Create a VideoCapture object
vc = cv2.VideoCapture(0)

# Create a function to update the video label
def update_video():
    ret, frame = vc.read()
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    label.config(image=imgtk)
    label.image = imgtk
    label.after(10, update_video)

update_video()

root.mainloop()