import os
import cv2
import pyautogui
import numpy as np
import google.generativeai as genai
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
from threading import Thread
import time
import pyttsx3
import pyperclip
import markdown
from tkhtmlview import HTMLLabel

genai.configure(api_key=os.environ['API_KEY'])

recording = False
video_file_name = "screen_recording.mp4"
fps = 20.0
codec = cv2.VideoWriter_fourcc(*"mp4v")

engine = pyttsx3.init()
is_playing = False

def start_recording():
    global recording, video_file_name
    recording = True
    screen_size = pyautogui.size()
    out = cv2.VideoWriter(video_file_name, codec, fps, screen_size)

    status_label.config(text="Screen recording started...")
    while recording:
        img = ImageGrab.grab(bbox=(0, 0, screen_size.width, screen_size.height))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
        time.sleep(1 / fps)

    out.release()
    status_label.config(text="Screen recording stopped.")
    start_wave_loading()
    process_video()

def stop_recording():
    global recording
    recording = False

def process_video():
    try:
        prompt = prompt_entry.get().strip()
        if not prompt:
            messagebox.showerror("Error", "Please enter a prompt before processing the video.")
            return

        print(f"Uploading file...")
        video_file = genai.upload_file(path=video_file_name)
        print(f"Completed upload: {video_file.uri}")

        while video_file.state.name == "PROCESSING":
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)

        model = genai.GenerativeModel(model_name="gemini-1.5-pro")

        response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
        status_label.config(text="Response received.")
        stop_wave_loading()

        html_content = markdown.markdown(response.text.strip())

        response_label.set_html(html_content)

        play_button.pack(side=tk.LEFT, padx=5, pady=10)
        stop_button_audio.pack(side=tk.LEFT, padx=5, pady=10)
        copy_button.pack(side=tk.LEFT, padx=5, pady=10)

        genai.delete_file(video_file.name)
        print(f'Deleted file {video_file.uri}')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def start_wave_loading():
    global loading_animation
    loading_animation = True
    animate_loading()

def stop_wave_loading():
    global loading_animation
    loading_animation = False

def animate_loading():
    if not loading_animation:
        loading_canvas.delete("all")
        return

    canvas_width = loading_canvas.winfo_width()
    canvas_height = loading_canvas.winfo_height()
    wave_height = 10
    wave_length = 100
    wave_speed = 10

    for i in range(0, canvas_width + wave_length, wave_speed):
        loading_canvas.delete("all")
        for j in range(0, wave_length, 20):
            x1 = i - wave_length + j
            x2 = x1 + 20
            y1 = canvas_height / 2 - wave_height
            y2 = canvas_height / 2 + wave_height
            loading_canvas.create_oval(x1, y1, x2, y2, fill="blue")
        loading_canvas.update()
        time.sleep(0.05)
        if not loading_animation:
            break

    if loading_animation:
        root.after(100, animate_loading)

def on_start_button_click():
    start_thread = Thread(target=start_recording)
    start_thread.start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

def on_stop_button_click():
    stop_recording()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def play_audio():
    global is_playing
    if not is_playing:
        try:
            engine.say(response_label.get("1.0", tk.END))
            engine.runAndWait()
            is_playing = True
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while playing audio: {str(e)}")

def stop_audio():
    global is_playing
    if is_playing:
        try:
            engine.stop()
            is_playing = False
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while stopping audio: {str(e)}")

def copy_to_clipboard():
    try:
        pyperclip.copy(response_label.get("1.0", tk.END).strip())
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while copying text: {str(e)}")

def on_enter(event):
    event.widget.config(bg='#C71585')  

def on_leave(event):
    event.widget.config(bg='#4CAF50')  

root = tk.Tk()
root.title("Smart Screen AI")

root.geometry("800x650") 

root.configure(bg='#f0f0f0')

status_label = tk.Label(root, text="Ready to record.", font=('Helvetica', 16), bg='#f0f0f0')
status_label.pack(pady=5)
          
prompt_label = tk.Label(root, text="Enter Prompt 💬:", font=('Helvetica', 14), bg='#f0f0f0')
prompt_label.pack(pady=5)
prompt_entry = tk.Entry(root, font=('Helvetica', 14), width=50)
prompt_entry.pack(pady=5)

start_button = tk.Button(root, text="Start Recording 🎥", command=on_start_button_click, font=('Helvetica', 14), bg='#4CAF50', fg='white', padx=5, pady=5)
start_button.pack(pady=5)
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

stop_button = tk.Button(root, text="Stop Recording ⏹️", command=on_stop_button_click, state=tk.DISABLED, font=('Helvetica', 14), bg='#F44336', fg='white', padx=5, pady=5)
stop_button.pack(pady=5)
stop_button.bind("<Enter>", on_enter)
stop_button.bind("<Leave>", on_leave)

loading_canvas = tk.Canvas(root, width=200, height=50, bg="white", highlightthickness=0)
loading_canvas.pack(pady=5)

html_frame = tk.Frame(root)
html_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

canvas = tk.Canvas(html_frame, bg='#f9f9f9', highlightthickness=0)
scroll_y = tk.Scrollbar(html_frame, orient="vertical", command=canvas.yview)
scroll_x = tk.Scrollbar(html_frame, orient="horizontal", command=canvas.xview)

response_frame = tk.Frame(canvas, bg='#f9f9f9')
response_label = HTMLLabel(response_frame, html="", width=80, height=120000)  
response_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas.create_window((0, 0), window=response_frame, anchor="nw")
response_frame.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_y.pack(side=tk.RIGHT, fill="y")
scroll_x.pack(side=tk.BOTTOM, fill="x")
canvas.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

play_button = tk.Button(root, text="▶️", command=play_audio, font=('Helvetica', 14), bg='#2196F3', fg='white', padx=5, pady=5)
play_button.pack(side=tk.LEFT, padx=5, pady=10)
play_button.bind("<Enter>", on_enter)
play_button.bind("<Leave>", on_leave)

stop_button_audio = tk.Button(root, text="⏹️", command=stop_audio, font=('Helvetica', 14), bg='#FF5722', fg='white', padx=5, pady=5)
stop_button_audio.pack(side=tk.LEFT, padx=5, pady=10)
stop_button_audio.bind("<Enter>", on_enter)
stop_button_audio.bind("<Leave>", on_leave)

copy_button = tk.Button(root, text="📋", command=copy_to_clipboard, font=('Helvetica', 14), bg='#009688', fg='white', padx=5, pady=5)
copy_button.pack(side=tk.LEFT, padx=5, pady=10)
copy_button.bind("<Enter>", on_enter)
copy_button.bind("<Leave>", on_leave)

root.mainloop()
