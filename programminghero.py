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
import pywhatkit
import datetime
import wikipedia

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
whisper_model = whisper.load_model("medium")

# Google Gemini API setup
GOOGLE_API_KEY = 'AIzaSyA4P2D967E4JzIo977DX97PAfralZKSnQU'
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
    modified_prompt = f"Give me a shorten answer to this question ({question}) in a maximum of 50 words."
    try:
        response = model.generate_content(modified_prompt)
        if response and hasattr(response, 'text'):
            print(f'ASK GEMINI RESPONSE: {response.text}')
            return response.text
        else:
            return "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"An error occurred while asking the AI: {str(e)}"

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

personal_list = ['who are you?', 'who are you', 'who created you?', 'who created you', 'who you are', 'Who you are?']

# Voice assistant loop encapsulated in a function
def run_assistant():
    try:
        while True:
            try:
                # Listen for voice input
                with sr.Microphone() as source:
                    print('Listening...')
                    listener.adjust_for_ambient_noise(source)
                    voice = listener.listen(source)

                    # Save the voice input to a temporary file for Whisper processing
                    with open("voice_input.wav", "wb") as f:
                        f.write(voice.get_wav_data())

                    # Transcribe the audio using Whisper
                    whisper_result = whisper_model.transcribe("voice_input.wav")
                    transcription = whisper_result["text"]
                    print("Whisper Transcription result:", transcription)
                    command = transcription.lower()

                    # Check if the command is a personal question
                    personal_question = any(personal in command for personal in personal_list)

                    if personal_question:
                        speak_and_print("I am a personal assistant created by you!")
                        print('\n\n')
                        time.sleep(5)
                        continue  # Skip the rest of the loop for personal questions

                    # Check if the command contains 'play' or 'playing'
                    if 'play' in command or 'playing' in command:
                        song = command.replace('play', '').replace('playing', '')
                        speak_and_print(f'Playing {song.strip()} on YouTube...')
                        pywhatkit.playonyt(song.strip())
                        print('\n\n')
                        # Add a delay after the AI response
                        time.sleep(180)
                    
                    elif 'time' in command:
                        current__time = datetime.datetime.now().strftime('%I:%M %p')
                        speak_and_print('Current time is: ' + current__time)
                        print('\n\n')
                        time.sleep(5)
                    
                    # To trigger the wikipedia scenario, 
                    # please say "Who is (name of the person)", or say "what is (thing you want to know)"
                    elif 'what' or 'who' in command:
                        thing_to_find = command.replace('who is', '').replace('what is', '').replace('who are', '').replace('what are', '').replace('who is the', '').replace('what is the', '').replace('who are the', '').replace('what are the', '')
                        info = wikipedia.summary(thing_to_find, 1)
                        speak_and_print(info)
                        print('\n\n')
                        time.sleep(20)
                    
                    elif 'who are you?' or 'who are you' or 'who created you?' or 'who created you' or 'who you are' in command:
                        speak_and_print("I am a personal assistant created by you!")

                    else:
                        # If no 'play' or 'playing' keyword, run the normal chatbot function
                        ai_response = ask_gemini(transcription)
                        speak_and_print(f'{ai_response}')
                        print('\n\n')
                        # Add a delay after the AI response
                        time.sleep(20)

            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                print('\n\n')

                # Add a delay after the error message
                time.sleep(20)

            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                print('\n\n')

                # Add a delay after the error message
                time.sleep(20)

            except Exception as e:
                print(f"An error occurred: {e}")
                print('\n\n')

                # Add a delay after the error message
                time.sleep(20)

    except KeyboardInterrupt:
        speak_and_print("\nGoodbye! Enjoy the rest of your day!")
        
    # Reset ALSA error handler to default after script finishes
    asound.snd_lib_error_set_handler(None)

run_assistant()