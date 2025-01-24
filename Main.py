import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

def test_rtsp():
    username = username_entry.get()
    password = password_entry.get()
    ip = ip_entry.get()
    port = port_entry.get()
    
    if not username or not password or not ip or not port:
        messagebox.showerror("Input Error", "All fields are required.")
        return
    
    # Create RTSP URL
    rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}"
    messagebox.showinfo("RTSP URL", f"RTSP URL: {rtsp_url}")
    
    # Start capturing the RTSP stream using OpenCV
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        messagebox.showerror("Connection Error", "Unable to connect to the RTSP stream.")
        return

    def update_frame():
        ret, frame = cap.read()
        if ret:
            # Convert the frame to an image that can be displayed in Tkinter
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            
            # Update the label with the new image
            video_label.img = img
            video_label.config(image=img)
            
            # Call this function again after 10 ms
            video_label.after(10, update_frame)
        else:
            messagebox.showerror("Stream Error", "Failed to read frame from the RTSP stream.")
            cap.release()

    # Set up the video window
    video_label.grid(row=0, column=0, padx=10, pady=10)
    
    # Start displaying the stream
    update_frame()

# Create the main window
root = tk.Tk()
root.title("RTSP Stream Test")

# Create and place the widgets
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=2, padx=10, pady=10)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=1, padx=10, pady=10, sticky='e')
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=2, padx=10, pady=10)

ip_label = tk.Label(root, text="IP Address:")
ip_label.grid(row=2, column=1, padx=10, pady=10, sticky='e')
ip_entry = tk.Entry(root)
ip_entry.grid(row=2, column=2, padx=10, pady=10)

port_label = tk.Label(root, text="Port Number:")
port_label.grid(row=3, column=1, padx=10, pady=10, sticky='e')
port_entry = tk.Entry(root)
port_entry.grid(row=3, column=2, padx=10, pady=10)

# Test button
test_button = tk.Button(root, text="Test RTSP", command=test_rtsp)
test_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Label to display video
video_label = tk.Label(root)
video_label.grid(row=0, column=0, padx=10, pady=10, rowspan=5)

# Run the application
root.mainloop()
