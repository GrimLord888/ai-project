import os
import sys
import warnings
import time  # Import the time module for adding delay
import speech_recognition as sr
import whisper
import google.generativeai as genai
from ctypes import *
import pyttsx3


# Suppress ALSA warnings using a custom error handler
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass  # Suppress ALSA warnings by not doing anything

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

# Load ALSA shared library and set custom error handler
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

# Suppress the specific torch FutureWarning about `weights_only=False`
warnings.filterwarnings(
    "ignore",
    message="You are using `torch.load` with `weights_only=False`",
    category=FutureWarning
)

# Initialize recognizer and load Whisper model
listener = sr.Recognizer()
model = whisper.load_model("base")

try:
    # Listen for voice input
    with sr.Microphone() as source:
        print('Listening......')
        voice = listener.listen(source)

        # Recognize the command using Google API
        command = listener.recognize_google(voice)
        print("Google Speech Recognition result:", command)

        # Save the voice input to a temporary file for Whisper processing
        with open("voice_input.wav", "wb") as f:
            f.write(voice.get_wav_data())

        # Transcribe the audio using Whisper
        result = model.transcribe("voice_input.wav")
        print("Whisper Transcription result:", result["text"])

except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
except Exception as e:
    print(f"An error occurred: {e}")
