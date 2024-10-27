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
from assistant_v2 import run_assistant
from twilio.rest import Client
import random

# Twilio setup
account_sid = 'AC4cb381206c6c8e0ba80005e7b38987f9'
auth_token = 'a44f701d94aabfb5a05e097618743def'
twilio_number = '+18508885594'
emergency_contact = '+61405529391'

client = Client(account_sid, auth_token)

def send_warning_message(heart_rate):
    message_body = f"Warning: Heart rate is high at {heart_rate} BPM. Immediate attention needed!"
    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=emergency_contact
    )
    print(f"Sent message: {message.sid}")

# Initialize speech recognizer and Whisper model
listener = sr.Recognizer()
whisper_model = whisper.load_model("medium")

# Google Gemini API setup
GOOGLE_API_KEY = 'AIzaSyA4P2D967E4JzIo977DX97PAfralZKSnQU'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def speak(answer):
    # Ensure that the answer is not empty
    if not answer.strip():
        print("Error: No text provided for TTS.")
        return  # Exit if the text is empty or only contains spaces
    
    tts = gTTS(answer)
    tts.save('hello.mp3')
    playsound('hello.mp3')

def speak_and_print(text):
    # Start a new thread for speaking
    speak_thread = threading.Thread(target=speak, args=(text,))
    speak_thread.start()
    # Print the text at the same time
    print(text)

    # Wait for the speech thread to complete before continuing
    speak_thread.join()

# Start searching with Google Gemini
def ask_gemini(question):
    # modified_prompt = f"Give me a concise and brief answer to this question ({question}) in a maximum of 50 words"
    modified_prompt = f"Answer this question briefly: {question}"
    response = model.generate_content(modified_prompt)
    return response.text

# Play 45 seconds long music
def play_music():
    playsound('experience.mp3')

# Global flag to prevent "Are you okay?" from repeating after the first time of breathing exercise
initial_emotion_check_done = False

positive_emotion_list = ['yes', 'fine', 'good', 'satisfied', 'satisfying', 'satify', 'excited', 'delighted', 'joyful', 'joy', 'hopeful', 'hope', 'lucky',
                        'fortune', 'fortunate', 'bright', 'encouraging', 'motivated', 'pleased', 'glad', 'thankful', 'grateful', 'not bad', 'cheerful', 'smiling']

negative_emotion_list = ['stress', 'Stress', 'stressed', 'Stressed', 'pressure', 'Pressure', 'heart rate', 'Heart rate', 'heartrate', 'Heartrate', 'painful', 'Painful', 'sad', 'Sad',
                        'not good', 'Not good', 'angry', 'Angry', 'bad', 'Bad', 'cry', 'Cry', 'depressed', 'Depressed', 'suffered', 'Suffered', 'suffering', 'Suffering', 'suffer', 'Suffer',
                        'not happy', 'Not happy', 'not', 'frustrated', 'frustration', 'frustrating']

no_list = ['no', 'No', 'nope', 'Nope', 'not', 'Not', 'not okay', 'Not okay', 'no okay', 'No okay', 'not OK', 'Not OK', 'not Ok', 'Not Ok', 'not good', 'Not good', 'bad', 'Bad', 'cry', 'Cry', 'disaster', 'Disaster', 'suffered', 'Suffered', 'suffering', 'Suffering', 'suffer', 'Suffer', 'sad', 'Sad', 'not happy', 'Not happy']

yes_list = ['yes', 'fine', 'good', 'satisfied', 'satisfying', 'satify', 'excited', 'delighted', 'joyful', 'joy', 'hopeful', 'hope', 'lucky', 'fortune', 'fortunate', 'bright', 'encouraging', 'motivated', 'pleased', 'glad', 'thankful', 'grateful', 'not bad', 'cheerful', 'smiling']

# Function to handle emotion-based responses
def handle_another_emotion_(command):
    # Check for positive emotions
    for word in positive_emotion_list:
        if word in command:
            speak_and_print("Keep going! I am rooting for you!")
            print('\n\n')
            # time.sleep(5)
            speak_and_print("However I realized your heart rate is high, let's us do some breathing exercises now.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Let’s start by taking a slow breath in through your nose.")
            print('\n')
            # time.sleep(15)
            speak_and_print("Now breathe out slowly through your mouth.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
            print('\n')
            # time.sleep(15)
            speak_and_print("Now breathe out through your mouth. Nice and slow.")
            print('\n')
            # time.sleep(20)
            speak_and_print("You’re doing well. One more time. Breathe in slowly.")
            print('\n')
            # time.sleep(15)
            speak_and_print("And breathe out slowly.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Good job! You did it great!")
            print('\n')
            # time.sleep(10)
            speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
            # time.sleep(10)
            print("Playing music......")
            play_music()
            print('\n\n')
            time.sleep(1)

            return True
    
    # Check for yes list
    for word in yes_list:
        if word in command:
            speak_and_print("Keep going! I am rooting for you!")
            print('\n\n')
            # time.sleep(5)
            speak_and_print("However I realized your heart rate is high, let's us do some breathing exercises now.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Let’s start by taking a slow breath in through your nose.")
            print('\n')
            # time.sleep(15)
            speak_and_print("Now breathe out slowly through your mouth.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
            print('\n')
            # time.sleep(15)
            speak_and_print("Now breathe out through your mouth. Nice and slow.")
            print('\n')
            # time.sleep(20)
            speak_and_print("You’re doing well. One more time. Breathe in slowly.")
            print('\n')
            # time.sleep(15)
            speak_and_print("And breathe out slowly.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Good job! You did it great!")
            print('\n')
            # time.sleep(10)
            speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
            # time.sleep(10)
            print("Playing music......")
            play_music()
            print('\n\n')
            time.sleep(1)

            return True

    # Check for negative emotions
    for word in negative_emotion_list:
        if word in command:
            speak_and_print("It's okay. Everything will be fine. You are not alone. I am here for you.")
            print('\n\n')
            # time.sleep(10)
            speak_and_print("To relieve your stress, let us start doing some breathing exercise now.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Let’s start by taking a slow breath in through your nose.")
            print('\n')
            # time.sleep(15)
            speak_and_print("Now breathe out slowly through your mouth.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
            print('\n')
            # time.sleep(15)
            speak_and_print("Now breathe out through your mouth. Nice and slow.")
            print('\n')
            # time.sleep(20)
            speak_and_print("You’re doing well. One more time. Breathe in slowly.")
            print('\n')
            # time.sleep(15)
            speak_and_print("And breathe out slowly.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Good job! You did it great!")
            print('\n')
            # time.sleep(5)
            speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
            # time.sleep(10)
            print("Playing music......")
            play_music()
            print('\n\n')
            time.sleep(1)
            
            return True
    
    # Check for no list
    for word in no_list:
        if word in command:
            speak_and_print("It's okay. Everything will be fine. You are not alone. I am here for you.")
            print('\n\n')
            # time.sleep(10)
            speak_and_print("To relieve your stress, let us start doing some breathing exercise now.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Let’s start by taking a slow breath in through your nose.")
            print('\n')
            # time.sleep(15)
            speak_and_print("Now breathe out slowly through your mouth.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
            print('\n')
            # time.sleep(15)
            speak_and_print("Now breathe out through your mouth. Nice and slow.")
            print('\n')
            # time.sleep(20)
            speak_and_print("You’re doing well. One more time. Breathe in slowly.")
            print('\n')
            # time.sleep(15)
            speak_and_print("And breathe out slowly.")
            print('\n')
            # time.sleep(20)
            speak_and_print("Good job! You did it great!")
            print('\n')
            # time.sleep(10)
            speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
            # time.sleep(10)
            print("Playing music......")
            play_music()
            print('\n\n')
            time.sleep(1)
            
            return True

    return False  # Return False if no emotion was detected

# Function of asking are you okay
# If the assistant does not understand the speech, it will call this function again until it gets a proper response or triggers the emergency timeout.
# The function returns True once a valid response is processed or after the emergency message is printed, which breaks the loop.
def ask_are_you_okay():
    global initial_emotion_check_done
    if initial_emotion_check_done:
        return  # Prevent re-asking once initial emotion check is done

    try:
        speak_and_print("Are you okay?")
        
        # Introduce a short delay to allow the assistant to finish speaking before listening
        time.sleep(2)

        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)

            try:
                # Listen for user input with a timeout of 5 seconds
                voice = listener.listen(source, timeout=5, phrase_time_limit=5)
                response = listener.recognize_google(voice).lower()
                print(f'User response: {response}')

                # Check if the response is too short or matches the assistant's own question
                if len(response.strip()) < 3 or "are you okay" in response:
                    print("Invalid response detected (possibly from the assistant's own voice). Asking again...")
                    return ask_are_you_okay()  # Recursively ask the question again
                
                handle_another_emotion_(response)
                return True  # If valid response, stop the loop

            except sr.WaitTimeoutError:
                # Trigger emergency action if no response is received within 5 seconds
                print("Emergency! No response received. Sending an emergency text message now......")
                speak_and_print("Emergency! No response received. Sending an emergency text message now......")
                time.sleep(10)
                return True  # Stop the loop after the emergency message

    except sr.UnknownValueError:
        # If the speech is detected but not understood or if no valid speech
        print("Sorry, I could not understand the audio. Asking again...")
        time.sleep(2)
        return ask_are_you_okay()  # Recursively ask the question again

# Main thing
# heartrate = input ("Enter your heart rate: ")
# print('\n')

# if heartrate >= 100:
#     # 2) Danger heart rate (heart rate > 100): Two subsections
#     # Voice assistant will ask "Are you okay?"
#     # a) If response (OK or not OK), Do the breathing exercise, and play the music
#     # b) If no response (Send emergency text): Send emergency text, stop. 
#     print('\n')
# else:
#     run_assistant()

# heartrate = int(input("Enter your heart rate: "))  # Ensure heartrate is an integer
# print('\n')

# Function to handle emergency situations if no response is received
def send_emergency_text():
    print("Emergency! No response received. Sending an emergency text message now......")
    speak_and_print("Emergency! No response received. Sending an emergency text message now......")
    time.sleep(10)

# Function to simulate random heart rate readings
def generate_heart_rate():
    return random.randint(50, 150)  # Normal range 60-100, abnormal above 100

# Main function to monitor and respond based on heart rate
def monitor_heart_rate():
    while True:
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
        # heartrate = generate_heart_rate()  # Automatically generate heart rate
        heartrate = 126
        print(f"Generated heart rate: {heartrate}\n")

        if heartrate >= 100:

            try:
                speak_and_print("Are you okay?")
                
                # Introduce a short delay to allow the assistant to finish speaking before listening
                time.sleep(3)

                with sr.Microphone() as source:
                    print('Listening...')
                    listener.adjust_for_ambient_noise(source)

                    try:
                        # Listen for user input with a timeout of 5 seconds
                        voice = listener.listen(source, timeout=5, phrase_time_limit=5)
                        response = listener.recognize_google(voice).lower()
                        print(f'User response: {response}')

                        # # Check if the response is too short or matches the assistant's own question
                        # if len(response.strip()) < 3 or "are you okay" in response:
                        #     print("Invalid response detected (possibly from the assistant's own voice). Asking again...")
                        #     ask_are_you_okay()  # Recursively ask the question again
                        # Check if the response is too short or matches the assistant's own question
                        if "are you okay" in response:
                            print("Invalid response detected (possibly from the assistant's own voice). Asking again...")
                            ask_are_you_okay()  # Recursively ask the question again
                        
                        handle_another_emotion_(response)

                    except sr.WaitTimeoutError:
                        # Trigger emergency action if no response is received within 5 seconds
                        print("Emergency! No response received. Sending an emergency text message now......")
                        speak_and_print("Emergency! No response received. Sending an emergency text message now......")
                        time.sleep(5)
                        send_warning_message(heartrate)
                        time.sleep(10)

            except sr.UnknownValueError:
                # If the speech is detected but not understood or if no valid speech
                print("Sorry, I could not understand the audio. Asking again...")
                time.sleep(2)
                ask_are_you_okay()  # Recursively ask the question again
            
            except KeyboardInterrupt:
                speak_and_print("\nGoodbye! Enjoy the rest of your day!")

        else:
            run_assistant()  # If heart rate is normal, proceed with normal assistant tasks

        time.sleep(2)  # Add a delay before generating the next heart rate

        # Reset ALSA error handler to default after script finishes
        asound.snd_lib_error_set_handler(None)

# Run the heart rate monitor
monitor_heart_rate()