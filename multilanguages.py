import os
import sys
import warnings
import time  # Import the time module for adding delay
import speech_recognition as sr
import whisper
import google.generativeai as genai
from ctypes import *
from gtts import gTTS
from playsound import playsound
import threading

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

# Initialize speech recognizer and Whisper model
listener = sr.Recognizer()
base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
whisper_model = whisper.load_model(base_model_path)

# Google Gemini API setup
GOOGLE_API_KEY = 'AIzaSyC1nBfI_nCRvsLVfkyGaxuxbpnyN0BMxX8'
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# Initialize Gemini AI model for conversation
model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)

# Generate shorter response
def ask_gemini(question):
  modified_prompt = f"Give me an shorten answer to this question ({question}) in maximum of 50 words"
  response = model.generate_content(modified_prompt)
  return response.text

def speak(answer):
    tts = gTTS(answer)
    tts.save('hello.mp3')
    playsound('hello.mp3')

def speak_and_print(text):
    # Start a new thread for speaking
    speak_thread = threading.Thread(target=speak, args=(text,))
    speak_thread.start()
    # Print the text at the same time
    print(text)

# Voice assistant loop
try:
    while True:
        try:
            # Listen for voice input
            with sr.Microphone() as source:
                print('Listening...')
                voice = listener.listen(source)

                # Save the voice input to a temporary file for Whisper processing
                with open("voice_input.wav", "wb") as f:
                    f.write(voice.get_wav_data())

                # Transcribe the audio using Whisper
                whisper_result = whisper_model.transcribe("voice_input.wav")
                transcription = whisper_result["text"]
                print("Whisper Transcription result:", transcription)

                # Send transcribed text to the AI model (Gemini)
                print('Sending prompt to AI model...')
                ai_response = ask_gemini(transcription)
                speak_and_print(f'{ai_response}')
                print('\n\n')

                # Add a delay after the AI response
                time.sleep(30)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            print('\n\n')

            # Add a delay after the error message
            time.sleep(30)

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            print('\n\n')

            # Add a delay after the error message
            time.sleep(30)

        except Exception as e:
            print(f"An error occurred: {e}")
            print('\n\n')

            # Add a delay after the error message
            time.sleep(30)

except KeyboardInterrupt:
    speak_and_print("\nGoodbye! Enjoy the rest of your day!")

# Reset ALSA error handler to default after script finishes
asound.snd_lib_error_set_handler(None)
