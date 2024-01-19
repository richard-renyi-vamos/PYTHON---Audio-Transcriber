import pyaudio
import wave
import speech_recognition as sr
import tkinter as tk

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

# Audio recording function
def record_audio():
    audio = pyaudio.PyAudio()

    # Start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

# Transcribe audio to text
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            text = f"Could not request results from Google Speech Recognition service; {e}"
    return text

# Function to update the GUI with transcribed text
def update_text():
    record_audio()
    transcribed_text = transcribe_audio()
    text_widget.insert(tk.END, transcribed_text + '\n')

# Set up the GUI
root = tk.Tk()
root.title("Audio Transcription")

text_widget = tk.Text(root)
text_widget.pack()

# Button to start transcription
transcribe_button = tk.Button(root, text="Transcribe", command=update_text)
transcribe_button.pack()

root.mainloop()
