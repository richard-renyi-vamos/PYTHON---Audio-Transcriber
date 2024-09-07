import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(file_path) as audio_file:
        audio_data = recognizer.record(audio_file)
        try:
            transcription = recognizer.recognize_google(audio_data)
            return transcription
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError as e:
            return f"Error with the transcription service: {e}"

def select_file():
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.wav *.mp3")])
    if file_path:
        file_label.config(text=os.path.basename(file_path))
        file_path_var.set(file_path)

def transcribe_file():
    file_path = file_path_var.get()
    if file_path:
        ext = os.path.splitext(file_path)[1]
        wav_file = file_path

        # Convert to WAV if needed
        if ext == ".mp3":
            wav_file = os.path.splitext(file_path)[0] + ".wav"
            sound = AudioSegment.from_mp3(file_path)
            sound.export(wav_file, format="wav")
        
        transcription = transcribe_audio(wav_file)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, transcription)
    else:
        messagebox.showerror("Error", "Please select a file first.")

# GUI setup
root = tk.Tk()
root.title("Audio Transcription Tool")

file_path_var = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=20)

file_label = tk.Label(frame, text="No file selected", width=40)
file_label.grid(row=0, column=0, padx=10)

select_button = tk.Button(frame, text="Select File", command=select_file)
select_button.grid(row=0, column=1, padx=10)

transcribe_button = tk.Button(root, text="Transcribe", command=transcribe_file)
transcribe_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=60)
result_text.pack(padx=20, pady=10)

# Start the GUI loop
root.mainloop()
